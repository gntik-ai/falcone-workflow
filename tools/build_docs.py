#!/usr/bin/env python3
"""Build requirements and GitHub backlog from the reviewed planning source."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / 'docs/planning-source.json').read_text())
requirements, issues = [], []
req_md = ['# 2. Functional requirements', '', 'Proposed requirements for a custom Falcone service. M0 confirms unresolved scope; inclusion is not proof of implementation.', '']
backlog_md = ['# 4. Implementation backlog', '', '12 epics, 36 stories; effort S/M/L is relative, not a delivery estimate. M0 discovery; M1 durable core; M2 integration; M3 migration and qualification.', '']
for category in data['categories']:
    code, name = category['code'], category['name']
    epic_id = 'EP-' + code
    children = []
    req_md += ['## ' + name, '']
    for n, story in enumerate(category['stories'], 1):
        sid = f'{code}-{n:02}'
        rids = []
        for j, statement in enumerate(story['requirements'], 1):
            rid = f'FR-{code}-{(n-1)*2+j:02}'
            requirements.append(dict(id=rid, category=code, statement=statement))
            rids.append(rid)
            req_md += [f'- [ ] **{rid}:** {statement}']
        body = f'<!-- falcone-workflow:{sid} -->\n\n## User story\n\n{story["story"]}\n\n## Description\n\n{story["description"]}\n\n## Acceptance criteria\n\n'
        body += '\n'.join('- [ ] ' + ac for ac in story['acceptance'])
        body += f'\n\n## Planning\n\n- Parent: {epic_id}\n- Phase: {story["phase"]}\n- Effort: {story["effort"]}\n- Depends on: ' + (', '.join(story['dependencies']) or 'None')
        body += '\n\n## Requirements\n\n' + '\n'.join(f'- **{rid}:** {s}' for rid, s in zip(rids,story['requirements'])) + '\n'
        children.append(dict(id=sid,type='story',title=f'[falcone-workflow][{sid}] {story["title"]}',body=body,parent=epic_id,requirements=rids,dependencies=story['dependencies'],phase=story['phase'],effort=story['effort'],labels=['falcone-workflow','type:story','area:'+code.lower(),'phase:'+story['phase'].lower(),'effort:'+story['effort'].lower()]))
    eb = f'<!-- falcone-workflow:{epic_id} -->\n\n## Goal\n\n{category["goal"]}\n\n## Stories\n\n' + '\n'.join('- '+c['id']+' — '+c['title'].split('] ')[-1] for c in children) + '\n\n## Completion\n\nAll child acceptance criteria pass; evidence is linked and unresolved compatibility differences are approved before cutover.\n'
    issues.append(dict(id=epic_id,type='epic',title=f'[falcone-workflow][{epic_id}] {name}',body=eb,parent=None,labels=['falcone-workflow','type:epic','area:'+code.lower()]))
    issues.extend(children)
    backlog_md += [f'- **{epic_id} — {name}**', '', category['goal'], '']
    for c in children:
        backlog_md += ['## '+c['id']+' — '+c['title'].split('] ')[-1], '', c['body'], '']
ids = {x['id'] for x in issues}
assert len(ids) == 48 and len(requirements) == 72
graph = {x['id']: x.get('dependencies',[]) for x in issues}
done, visiting = set(), set()
def visit(k):
    assert k in ids and k not in visiting, f'Invalid dependency or cycle: {k}'
    if k in done: return
    visiting.add(k)
    for dep in graph[k]: visit(dep)
    visiting.remove(k); done.add(k)
for k in graph: visit(k)
assert {r['id'] for r in requirements} == {r for x in issues for r in x.get('requirements',[])}
out = dict(schema_version=1,project='falcone-workflow',status='proposed',baseline_commit=data['baseline_commit'],requirements=requirements,issues=issues)
(ROOT/'docs/backlog.json').write_text(json.dumps(out,indent=2)+'\n')
(ROOT/'docs/requirements.md').write_text('\n'.join(req_md)+'\n')
(ROOT/'docs/backlog.md').write_text('\n'.join(backlog_md)+'\n')
print(f'Validated {len(requirements)} requirements, {len(issues)} issues and acyclic dependencies.')
