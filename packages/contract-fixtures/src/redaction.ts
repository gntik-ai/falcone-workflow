/** All captured identity, credential and payload strings must use these placeholders. */
export const PLACEHOLDER = /^<redacted:[a-z][a-z0-9-]*>$/;

export function assertRedacted(value: unknown): void {
  function visit(item: unknown, sensitive = false): void {
    if (typeof item === "string") {
      if ((sensitive && !PLACEHOLDER.test(item)) ||
          /bearer\s+\S+|-----BEGIN [A-Z ]*PRIVATE KEY-----|\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.|\b(?:sk|ghp|github_pat)[-_][A-Za-z0-9_-]{12,}/i.test(item)) {
        // Never include the rejected value in diagnostics.
        throw new Error("Fixture redaction violation");
      }
    } else if (Array.isArray(item)) {
      item.forEach(child => visit(child, sensitive));
    } else if (item !== null && typeof item === "object") {
      for (const [key, child] of Object.entries(item)) {
        const normalized = key.replace(/[-_]/g, "");
        if (/bearer\s/i.test(key)) throw new Error("Fixture redaction violation");
        const identity = /^(tenant|workspace|run)(id|identifier|uuid)?$/i.test(normalized);
        const secret = /secret|password|token|authorization|apikey|privatekey|cookie|credential/i.test(normalized);
        visit(child, sensitive || identity || secret || /payload|body/i.test(normalized));
        if ((identity || secret) && typeof child !== "string") {
          throw new Error("Fixture identities and credentials require placeholders");
        }
      }
    }
  }
  visit(value);
}
