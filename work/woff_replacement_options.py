"""Catalogue choices and one-shot controls; no obsolete replacement hooks."""
import json
from pathlib import Path

# Curated species classifications, not inferred from library membership or
# undocumented character columns. Sources and limits: WOFF_DROPDOWN_PROGRESS.md.
LEGIT_IDS = {7025, 7031, 7073}  # Goblin, Chocochick, Mu: user-owned captures.
LEGIT_REWARDS = {8028, 8018, 8017}  # Garland, Lich, Marilith.
LEGIT_GIFTS = {7000, 7149}  # Tama, Serafie.
LEGIT_TRANSFIGURATIONS = {7003}  # Tamamohime.
BOSS_ONLY_IDS = {7194, 7193, 7195, 7027, 7113, 7041, 7172,
                 7162, 7191, 7080, 8025, 8032}


def ownership_status(r):
    ident = r['id']
    if 'UNUSED LABEL' in r['status']:
        return 'Unused entry / Save risk unverified'
    if 'TEST DEFINITION' in r['status']:
        return 'Hidden test variant / Save risk unverified'
    if ident in LEGIT_IDS:
        return 'Legit Mirage'
    if ident in LEGIT_REWARDS:
        return 'Legit Mirage (defeat reward, not direct capture)'
    if ident in LEGIT_GIFTS:
        return 'Legit Mirage (gift)'
    if ident in LEGIT_TRANSFIGURATIONS:
        return 'Legit Mirage (transfiguration)'
    if ident in BOSS_ONLY_IDS:
        return 'Not normally capturable / Save safety unverified'
    if not r['library_listed']:
        return 'Hidden or alternate entry / Ownership unverified'
    return 'Legit status unverified'


def candidates():
    records = json.loads(Path(__file__).with_name('woff-mirage-catalogue.json').read_text(encoding='utf-8'))
    return sorted((r for r in records if r['candidate']), key=lambda r: (r['name'].casefold(), r['id']))


def dropdown():
    rows = ['0:Select a Mirage first — no replacement']
    for r in candidates():
        status = ownership_status(r)
        if r.get('size_native')=='EX':
            status += '; EX summon'
        name = r['name'] if r['name'] != r['key'] else 'Unnamed Mirage'
        rows.append(f"{r['id']}:{name} [{r['size']}] - {status}")
    return '\n'.join(rows)


ARM = r'''[ENABLE]
{$lua}
if syntaxcheck then return end
local id=readInteger('WFF_NextCaptureID')
if not id or id==0 then error('Choose a Mirage in the dropdown before arming replacement.') end
{$asm}
WFF_NextCaptureArmed:
dd 1
[DISABLE]
WFF_NextCaptureArmed:
dd 0
'''
