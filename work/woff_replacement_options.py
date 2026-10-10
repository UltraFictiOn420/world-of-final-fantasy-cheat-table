"""Catalogue choices and one-shot controls; no obsolete replacement hooks."""
import json
from pathlib import Path


def candidates():
    records = json.loads(Path(__file__).with_name('woff-mirage-catalogue.json').read_text(encoding='utf-8'))
    return sorted((r for r in records if r['candidate']), key=lambda r: (r['name'].casefold(), r['id']))


def dropdown():
    rows = ['0:Select a Mirage first — no replacement']
    for r in candidates():
        warning = ''
        if 'UNUSED LABEL' in r['status']:
            warning = ' [UNUSED / EXPERIMENTAL]'
        elif 'TEST DEFINITION' in r['status']:
            warning = ' [TEST / EXPERIMENTAL]'
        elif not r['library_listed']:
            warning = ' [OUTSIDE LIBRARY / EXPERIMENTAL]'
        rows.append(f"{r['id']}:{r['name']} — {r['key']}, ID {r['hex_id']}{warning}")
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
