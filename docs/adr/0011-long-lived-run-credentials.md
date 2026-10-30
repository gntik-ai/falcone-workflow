# ADR-0011: Long-lived run authority, renewal and revocation

Status: Proposed

## Context

[architecture.md, Long-lived credentials and payloads](../architecture.md#long-lived-credentials-and-payloads) proposes execution authority references instead of unlimited user tokens. [architecture.md, Typical invocation](../architecture.md#typical-invocation) requires short-lived credentials resolved through authoritative lineage. FR-TEN-03, FR-TEN-04, FR-ACT-06 and FR-HUM-09 affect TEN-02 (#35), ACT-03 (#24) and HUM-03 (#33).

## Decision

Propose storing an opaque execution authority reference with authoritative tenant, workspace, root-run and permitted child/attempt lineage. Resolve it from committed run/task state, never workflow inputs or caller-supplied ancestry. At each external effect, an authorized worker obtains a short-lived task-scoped capability through Falcone's credential service under current policy. No bearer token or secret value enters plans, checkpoints, event history, logs or SSE.

Renewal across login/session or offline-token expiry is policy-controlled reauthorization, not extension of a captured login token. Persist only sanitized status and reference metadata. Credential-service unavailability or inability to prove current authorization fails closed for new effects and opens a typed policy-blocked or credential incident. Preserve waiting state and already committed outcomes.

Propose that user/role revocation blocks newly unauthorized effects rather than silently cancelling the entire run. Renewal and each dispatch recheck current authority; a capability's bounded validity and revocation propagation require an owner-confirmed service contract. Already issued remote effects cannot be undone by local revocation. Expose that limitation and qualify the revocation window before production, without inventing a credential-service API here.

Controlled reauthorization requires a verified authorized actor, reason, expected revision and an audited new authority binding consistent with original tenant/workspace lineage. It cannot move a run across tenants or reset an ambiguous non-idempotent effect for blind retry. Recheck credentials for cleanup/compensation as well as normal tasks; do not retain a privileged emergency token in workflow state.

Acceptance requires R3 review with a second reviewer (Security engineers) and explicit operator approval. Falcone integration team confirms renewal/revocation behavior; Workflow/runtime maintainers enforce lineage; Release/QA maintainers exercise forged ancestry, foreign workspace, role revocation, expiry crossing, service outage and controlled reauthorization.

## Alternatives

- Persisting user tokens for the duration of multi-month runs creates unbounded credential exposure.
- Trusting lineage supplied in workflow input allows authority substitution.
- Cancelling all runs on logout changes business semantics and does not revoke completed effects.

## Consequences

Long-lived runs can remain parked until an accountable actor reauthorizes them. D8 wait support does not imply perpetual authorization. Credentials remain an external policy dependency owned by Falcone; this proposal neither reads nor changes credential material.
