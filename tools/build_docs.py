#!/usr/bin/env python3
"""Build requirements, the GitHub backlog and the combined design document from the
reviewed planning source and the hand-written chapters."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
DESIGN = 'falcone-workflow-design.md'
data = json.loads((DOCS / 'planning-source.json').read_text())

# Issue numbers are owned by the publisher and recorded in github-issues.md; items listed
# there as "(unpublished)" have no GitHub issue yet and are created by the next import.
index = (DOCS / 'github-issues.md').read_text()
published = {m[1]: int(m[2]) for m in re.finditer(
    r'\[([A-Z]{2,4}-\d\d) — [^\]]+\]\(https://github\.com/gntik-ai/falcone-workflow/issues/(\d+)\)', index)}
published.update({m[1]: int(m[2]) for m in re.finditer(r'^## (EP-[A-Z]{2,4}) — .*\n\nEpic: \[#(\d+)\]', index, re.M)})
unpublished = set(re.findall(r'^- ([A-Z]{2,4}-\d\d) — .* \(unpublished\)$', index, re.M))

requirements, issues = [], []
by_category = {}
for category in data['categories']:
    code, name = category['code'], category['name']
    epic_id = 'EP-' + code
    children = []
    by_category[code] = []
    for n, story in enumerate(category['stories'], 1):
        sid = f'{code}-{n:02}'
        rids, statements = [], []
        for j, item in enumerate(story['requirements'], 1):
            if isinstance(item, str):
                # The original package numbered two requirements per story by position.
                assert j <= 2, f'{sid}: positional requirement {j} must be given an explicit id'
                rid, statement = f'FR-{code}-{(n-1)*2+j:02}', item
            else:
                rid, statement = item['id'], item['statement']
            assert re.fullmatch(rf'FR-{code}-\d\d', rid), f'{sid}: requirement id {rid} is not in area {code}'
            by_category[code].append(dict(id=rid, category=code, statement=statement))
            rids.append(rid)
            statements.append(statement)
        body = f'<!-- falcone-workflow:{sid} -->\n\n## User story\n\n{story["story"]}\n\n## Description\n\n{story["description"]}\n\n## Acceptance criteria\n\n'
        body += '\n'.join('- [ ] ' + ac for ac in story['acceptance'])
        body += f'\n\n## Planning\n\n- Parent: {epic_id}\n- Phase: {story["phase"]}\n- Effort: {story["effort"]}\n- Depends on: ' + (', '.join(story['dependencies']) or 'None')
        body += '\n\n## Requirements\n\n' + '\n'.join(f'- **{rid}:** {s}' for rid, s in zip(rids, statements)) + '\n'
        children.append(dict(id=sid, type='story', title=f'[falcone-workflow][{sid}] {story["title"]}', body=body, parent=epic_id, requirements=rids, dependencies=story['dependencies'], phase=story['phase'], effort=story['effort'], labels=['falcone-workflow', 'type:story', 'area:'+code.lower(), 'phase:'+story['phase'].lower(), 'effort:'+story['effort'].lower()]))
    by_category[code].sort(key=lambda r: int(r['id'][-2:]))
    requirements += by_category[code]
    eb = f'<!-- falcone-workflow:{epic_id} -->\n\n## Goal\n\n{category["goal"]}\n\n## Stories\n\n' + '\n'.join('- '+c['id']+' — '+c['title'].split('] ')[-1] for c in children) + '\n\n## Completion\n\nAll child acceptance criteria pass; evidence is linked and unresolved compatibility differences are approved before cutover.\n'
    issues.append(dict(id=epic_id, type='epic', title=f'[falcone-workflow][{epic_id}] {name}', body=eb, parent=None, labels=['falcone-workflow', 'type:epic', 'area:'+code.lower()]))
    issues.extend(children)

# Validation: unique identities, complete requirement coverage, acyclic dependencies and a
# published-or-unpublished entry in github-issues.md for every issue.
issue_ids = [x['id'] for x in issues]
req_ids = [r['id'] for r in requirements]
assert len(set(issue_ids)) == len(issue_ids), 'duplicate issue id'
assert len(set(req_ids)) == len(req_ids), 'duplicate requirement id'
ids = set(issue_ids)
graph = {x['id']: x.get('dependencies', []) for x in issues}
done, visiting = set(), set()
def visit(k):
    assert k in ids and k not in visiting, f'Invalid dependency or cycle: {k}'
    if k in done: return
    visiting.add(k)
    for dep in graph[k]: visit(dep)
    visiting.remove(k); done.add(k)
for k in graph: visit(k)
assert set(req_ids) == {r for x in issues for r in x.get('requirements', [])}
assert not (set(published) & unpublished), 'an issue is both published and unpublished'
assert set(published) | unpublished == ids, f'github-issues.md does not match the backlog: {sorted(ids ^ (set(published) | unpublished))}'

epics = [x for x in issues if x['type'] == 'epic']
stories = [x for x in issues if x['type'] == 'story']
counts = f'{len(epics)} epics and {len(stories)} stories'
out = dict(schema_version=1, project='falcone-workflow', status='proposed', baseline_commit=data['baseline_commit'], requirements=requirements, issues=issues)

req_md = ['# 2. Functional requirements', '', f'{len(requirements)} testable requirements for a custom Falcone service. Requirements added by the 30 October 2026 functional gap analysis continue each area\'s numbering. Inclusion is not proof of implementation.', '']
backlog_md = ['# 4. Implementation backlog', '', f'{counts}; effort S/M/L is relative, not a delivery estimate. M0 discovery; M1 durable core; M2 integration; M3 migration and qualification.', '']
for category in data['categories']:
    code = category['code']
    req_md += ['## ' + category['name'], '']
    req_md += [f'- [ ] **{r["id"]}:** {r["statement"]}' for r in by_category[code]]
    req_md += ['']
    backlog_md += [f'- **EP-{code} — {category["name"]}**', '', category['goal'], '']
    for c in stories:
        if c['parent'] == 'EP-' + code:
            backlog_md += ['## '+c['id']+' — '+c['title'].split('] ')[-1], '', c['body'], '']
while req_md[-1] == '': req_md.pop()

# ------------------------------------------------------------------------------------
# Combined design document read by Hermes's backlog-decomposition inventory: §0 accepted
# direction, §1 survey, §2 requirements and §4 backlog by area subsection, §3 architecture,
# §5 open questions, §6 trade-offs and sequence, then sources. Chapters are embedded with
# their headings demoted one level so only this file's ## and ### lines structure it.
_FENCE = re.compile(r'^\s*(```|~~~)')

def embed(name):
    lines = (DOCS / name).read_text().rstrip('\n').split('\n')
    if lines and lines[0].startswith('# '):
        lines = lines[1:]
    result, fenced = [], False
    for line in lines:
        if _FENCE.match(line):
            fenced = not fenced
        elif not fenced and re.match(r'^#{1,5} ', line):
            line = '#' + line
        result.append(line)
    return '\n'.join(result).strip('\n')

def issue_ref(item_id):
    return f'#{published[item_id]}' if item_id in published else 'unpublished'

design = [
    '# falcone-workflow: native durable workflow engine design', '',
    '<!-- Generated by tools/build_docs.py from design.md, survey.md, planning-source.json, architecture.md, open-questions.md, tradeoffs.md, migration.md and sources.md. Do not edit by hand. -->', '',
    f'Planning status ({data["date"]}): {data["status"]}. {len(requirements)} requirements, {counts}.', '',
    '## Accepted direction and scope', '', embed('design.md'), '',
    '## 1. Survey and comparative analysis', '', embed('survey.md'), '',
    '## 2. Functional requirements checklist', '',
    f'{len(requirements)} testable statements in {len(epics)} areas. Every requirement maps to one story in section 4. Requirements added by the 30 October 2026 functional gap analysis continue each area\'s numbering; additive DSL features leave apiVersion v1.0 behavior unchanged.', '',
]
for category in data['categories']:
    design += [f'### {category["code"]}. {category["name"]}', '']
    design += [f'- [ ] **{r["id"]}:** {r["statement"]}' for r in by_category[category['code']]]
    design += ['']
design += ['## 3. Baseline architecture', '', embed('architecture.md'), '',
           '## 4. Detailed backlog', '',
           f'{counts}. Every story has a user story, description, acceptance criteria, requirement links, dependencies, phase and effort. Effort S/M/L is relative, not a delivery estimate. Phases: M0 discovery; M1 durable core; M2 Falcone completeness; M3 qualification and migration. Issue numbers come from github-issues.md; stories marked unpublished have no GitHub issue yet. A story that spans repositories is decomposed into one issue per repository (falcone-workflow, falcone, falcone-charts).', '']
for category in data['categories']:
    code = category['code']
    design += [f'### {code}. {category["name"]}', '', f'- **Epic EP-{code} ({issue_ref("EP-" + code)}): {category["goal"]}**', '']
    for c in stories:
        if c['parent'] != 'EP-' + code:
            continue
        source = category['stories'][int(c['id'][-2:]) - 1]
        design += [
            f'- **{c["id"]} — {c["title"].split("] ")[-1]}** · {c["effort"]} · {c["phase"]} · {issue_ref(c["id"])}',
            f'  - **Story:** {source["story"]}',
            f'  - **Description:** {source["description"]}',
            '  - **Acceptance:** ' + ' '.join(f'({n}) {text}' for n, text in enumerate(source['acceptance'], 1)),
            f'  - **Requirements:** {", ".join(c["requirements"])}. **Dependencies:** {", ".join(c["dependencies"]) or "None"}.',
            '',
        ]
design += ['## 5. Open questions and ownership', '', embed('open-questions.md'), '',
           '## 6. Trade-offs and sequence', '', embed('tradeoffs.md'), '',
           '### Migration and qualification sequence', '', embed('migration.md'), '',
           '## Sources and evidence', '', embed('sources.md')]
design_text = '\n'.join(design).rstrip('\n') + '\n'

# The structure Hermes's inventory requires (decomposition_inventory.design_sections):
# unique `##` sections and `###` subsection keys, sections 0, 3, 5 and 6, and an
# `AREA.` subsection for every epic in sections 2 and 4.
def slug(title):
    return re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60] or 'section'
sections, current, fenced, numbered_seen = {}, None, False, False
for line in design_text.split('\n'):
    if _FENCE.match(line):
        fenced = not fenced
    heading = None if fenced else re.match(r'^(#{2,3}) +(\S.*?)\s*$', line)
    if heading and len(heading[1]) == 2:
        numbered = re.match(r'^([0-9]{1,2})\.\s+(\S.*)$', heading[2])
        numbered_seen = numbered_seen or numbered is not None
        key = str(int(numbered[1])) if numbered else ('0' if not numbered_seen else slug(heading[2]))
        assert key not in sections, f'{DESIGN}: section {key} appears twice'
        current = sections[key] = []
    elif heading:
        assert current is not None, f'{DESIGN}: subsection before any section'
        area = re.match(r'^([A-Z]{2,4})\.\s+(\S.*)$', heading[2])
        key = area[1] if area else slug(heading[2])
        assert key not in current, f'{DESIGN}: subsection {key} repeats'
        current.append(key)
for key in ('0', '3', '5', '6'):
    assert key in sections, f'{DESIGN}: section {key} is missing'
for key in ('2', '4'):
    missing = {x['id'][3:] for x in epics} - set(sections.get(key, []))
    assert not missing, f'{DESIGN}: section {key} lacks area subsections {sorted(missing)}'

(DOCS / 'backlog.json').write_text(json.dumps(out, indent=2) + '\n')
(DOCS / 'requirements.md').write_text('\n'.join(req_md) + '\n')
(DOCS / 'backlog.md').write_text('\n'.join(backlog_md) + '\n')
(DOCS / DESIGN).write_text(design_text)
print(f'Validated {len(requirements)} requirements, {len(issues)} issues ({len(unpublished)} unpublished), acyclic dependencies and the {DESIGN} structure.')
