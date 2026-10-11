"""Curated backup: no game assets, raw matrices, saves or local diagnostics."""
from pathlib import Path
import json
import hashlib
import xml.etree.ElementTree as E
ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'outputs/github-projects/world-of-final-fantasy-cheat-table'

def main():
    files={}
    modules=['build_woff_table.py','woff_battle_scripts.py','woff_cost_item_scripts.py',
        'woff_capture_scripts.py','woff_replacement_v9.py','woff_replacement_options.py',
        'woff_save_script.py','woff_info_readonly.lua','woff_mirage_catalogue.py',
        'woff_loot_scripts.py','woff_status_scripts.py','woff_combat_extra_scripts.py',
        'woff_accuracy_script.py','woff_topple_script.py','test_woff_table.py',
        'test_woff_catalogue.py','ue3_inspect.py','package_woff_repository.py']
    for name in modules:files['work/'+name]=(ROOT/'work'/name).read_text(encoding='utf-8')
    records=json.loads((ROOT/'work/woff-mirage-catalogue.json').read_text(encoding='utf-8'))
    files['work/woff-mirage-catalogue.json']=json.dumps([{k:v for k,v in r.items() if k!='raw_cells'}
        for r in records],ensure_ascii=False,indent=2)+'\n'
    latest=ROOT/'outputs'/'World of Final Fantasy - Original v29.CT'
    files['outputs/'+latest.name]=latest.read_text(encoding='utf-8')
    for version in range(1,29):
        p=ROOT/'outputs'/f'World of Final Fantasy - Original v{version}.CT'
        if p.exists():files['archive/'+p.name]=p.read_text(encoding='utf-8')
    root=E.parse(latest)
    entries=root.findall('.//CheatEntry')
    def status(e):
        ident=int(e.findtext('ID'))
        if ident>=200:return 'organization folder; not a cheat'
        if ident in (83,84,85):return 'protected read-only information'
        if ident==118:return 'unavailable; possible crash, causality unconfirmed'
        if ident in (114,115):return 'unverified gameplay effect'
        if 80<=ident<=82:return 'experimental; Chocochick visuals/naming/ownership confirmed; broader safety unverified'
        if ident==117:return 'provisional; wobble may clear on next action'
        return 'see validation record; no universal certification'
    def category(ident):
        groups=[('Currency / SP',{10,11,20,21}),('XP',{30,31,32}),
            ('Battle / AP',{40,41,42,43,44,45,50,51,116}),
            ('Buffs / Stacks',{110,111,112,113,114,115,117,119}),
            ('Items / Loot',{60,61,62,100}),('Capture',set(range(70,86))),('Saving',{90})]
        return next((name for name,ids in groups if ident in ids),'Foundation / Organization / Unavailable')
    features=[{'id':int(e.findtext('ID')),'description':e.findtext('Description').strip('"'),
        'game':'World of Final Fantasy (Steam/PC)','category':category(int(e.findtext('ID'))),
        'code_type':'Auto Assembler / Lua' if e.find('AssemblerScript') is not None else
        ('Folder / information' if e.find('GroupHeader') is not None else e.findtext('VariableType')),
        'status':status(e)} for e in entries]
    files['catalog/features.json']=json.dumps(features,ensure_ascii=False,indent=2)+'\n'
    files['docs/usage.md']='# Current usage — v29\n\n'+root.findtext('Comments')+'\n'
    files['README.md']='''# World of Final Fantasy — Original Cheat Table

Steam/PC, developed with UltraFictiOn420 and AI assistance. Current snapshot: **v29**, 2026-10-11.
Ongoing project, not a universally tested final release.

## Download and start

[Download v29](outputs/World%20of%20Final%20Fantasy%20-%20Original%20v29.CT).
Open in Cheat Engine, attach to `WOFF.exe`, load a save, then enable the top **Enable First** entry.
Disable old cheats before loading another table. Back up saves; use separate slots for experimental changes.
Verified x64 executable: version 2.0.0.0, PE timestamp `5B9B7E76`; other builds are not certified.

## Features

| Section | Features / limitations |
| --- | --- |
| Currency / SP | Infinite Gil; ignore SP requirements; no SP deduction |
| XP / Levels | XP multiplier including 50000x; max level on positive XP; results visible after battle |
| Battle / AP | God Mode; max living-party HP/AP; one-hit kill; player/enemy damage multipliers; infinite/zero-cost AP; critical hits |
| Buffs / Stacks | Haste/Regen/Protect/Shell before first action; never topple; F8 enemy topple; duration/negative-status options unverified |
| Items / Loot | Infinite usage; never below one; positive-chance alternative enemy drops, native quantities |
| Capture | Easy Imprism including Prism/permission bypass; one replacement per battle; species-size-status dropdown |
| Saving | Field Save Anywhere; reopen menu; separate save recommended |
| Unavailable | Never Miss: no active patch, possible crash causality unconfirmed |

Chocochick replacement now shows the selected model during capture/naming, including its default name.
Other species, boards/abilities and replacement save/reload safety need broader testing.
Dropdown ownership classification is partial; unknown/hidden/test/unused entries are not certified safe.
F8 beep means queued, not completed; queue expires in three real seconds. Press before Defend/enemy turn.
Never Topple may leave wobble animation until the next action. Champion cost zero is not implemented.

## Organization and development

- `outputs/`: current table only; `archive/`: historical snapshots, not recommended for play.
- `work/`: original source modules, builder, tests and curated catalogue metadata.
- `catalog/`: feature index; `docs/`: usage, testing, provenance and next steps.

32 local automated checks pass: 24 table/model checks plus 8 installed-catalogue checks.
Run `python work/build_woff_table.py`, then `python work/test_woff_table.py` for 24 non-live checks.
Catalogue tests additionally need installed game data. Optional live checks require Windows/pefile.
The developer memory helper can write memory; ordinary users do not need to run it.
v29 live folder rendering and revised information guard still need confirmation.

No game binaries/assets, saves, raw memory dumps, credentials or machine-specific installers are included.
Reference tables were studied for context; their scripts are not redistributed. Deleted research repo stays deleted.
[Launcher project](https://github.com/UltraFictiOn420/world-of-final-fantasy-launcher) remains separate.
See [usage](docs/usage.md), [testing](docs/testing.md), [next steps](docs/next-session.md), [history](CHANGELOG.md).
Offline single-player only; no warranty. This source backup is not a new GitHub Release.
'''
    files['docs/testing.md']='''# Validation — v29, 2026-10-11

32 automated checks pass: 24 table/model and 8 installed-catalogue checks. Not universal gameplay proof.
v29 compares all non-master scripts byte-for-byte with v28 and the master's assembly portion.
Only presentation/help and the UI-only information guard changed.

User-confirmed within tested scope: Gil/SP/XP, God Mode/AP, damage/max vitals, zero ability AP cost,
item modes, Mu/Chocochick/Behemoth capture, owned Chocochick/Goblin replacement, field save/reload,
critical hits and Mini Golem/Copper Gnome F8 topple. Never Topple remains provisional.
v22 buffs reached both observed stacks/all six members before an action; fresh-battle visuals confirmed.
Duration protection/negative-status blocking remain unverified. v23 repaired Never Topple's missing label.
v24 four-enemy loot test: 4 Potions, 3 Antidotes, 1 Wobblestopper, 50 Gil; eight native entries attempted,
six otherwise failing rolls bypassed. Native quantities/Gil unchanged; broader loot testing remains useful.
v27 Chocochick capture model, naming model/default name and owned species confirmed.
Other species and saved persistence remain unverified. v28 classifications are partial.
v29 live folder/guard behavior still needs confirmation. Never Miss unavailable after possible crash;
causality unconfirmed. No temporary observation trace ships in the current table.
'''
    files['docs/next-session.md']='''# Resume checkpoint — v29

- Confirm folders and read-only information guards after loading v29.
- Continue exact-species normal-obtainability classifications; library presence is not ownership proof.
- Validate replacement boards/abilities/battle behavior and separate-save/reload persistence.
- Test duration and negative-status protection separately.
- Implement champion cost zero when an available champion can be tested.
- Optional: bounded native loot quantities; no current quantity multiplier.
- Optional: investigate Never Miss only if proportionate; otherwise leave unavailable.
- Broader stack/topple, map/story saving and non-use item-removal testing remains.

Disable previous cheats before loading another table. Keep launcher separate and deleted research repo deleted.
'''
    files['docs/research.md']='''# Provenance and limits

Original scripts independently inspected against native routines; reference tables used for context only.
Replacement uses selected-species clone construction, early bounded naming preparation and native owned grant.
No source-enemy identity overwrites or existing-owned-Mirage rewrites. Catalogue independently decoded from
installed definitions; raw cell matrices/assets excluded. LL/EX display XL; EX summons explicitly distinguished.
Library membership does not prove normal ownability or save safety. Hidden entries remain unverified.
Temporary diagnostics, local bridge installers and machine-specific logs stay local.
'''
    files['CHANGELOG.md']='''# Version history

| Version | Milestone / caution |
| --- | --- |
| v1–v7 | Foundation, Gil/SP/XP, combat/AP/items, Easy Imprism and Prism bypass |
| v8 | Failed visual-only replacement; do not use |
| v9–v10 | Owned-grant replacement; protected information rows |
| v11 | Field saving prototype with disable bug; do not use |
| v12–v13 | Save disable repair and clean backup |
| v14–v18 | Loot/status/critical experiments; capture permission and stack-member buffs repaired |
| v19–v21 | F8 game-thread topple, expiring queue/beep; Never Miss quarantined |
| v22 | Selected buffs before first action, fresh-battle visuals confirmed |
| v23 | Never Topple missing label repaired |
| v24 | Positive-chance alternative enemy drops, native quantities; four-enemy test confirmed |
| v25 | Clean species-size dropdown |
| v26 | Capture visuals corrected; naming display still original; superseded |
| v27 | Early naming fix; Chocochick capture/naming/default name/ownership confirmed |
| v28 | Partial evidence-based ownership classifications; no unproven safety claims |
| v29 | Organized folders, current help, confirmed buff labels cleaned; gameplay hooks unchanged |

Use v29. Archives preserve development, not safe playable recommendations.
'''
    files['archive/README.md']='# Historical snapshots\n\nUse v29 in outputs. Old snapshots include bugs, diagnostics and failed experiments. Never load multiple table versions together.\n'
    files['.gitignore']='__pycache__/\n*.pyc\npydeps/\nprivate-backups/\nsaves/\n*.dmp\n*.log\n.env\n'
    files['requirements-dev.txt']='pefile\n# Optional Windows live checks only.\n'
    files['CHECKSUMS.sha256']=hashlib.sha256(latest.read_bytes()).hexdigest()+'  outputs/'+latest.name+'\n'
    for rel,content in files.items():
        p=DEST/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
    manifest=[{'path':rel,'mode':'100644','type':'blob','content':content} for rel,content in sorted(files.items())]
    (ROOT/'work/woff-github-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf-8')
    print(f'Curated {len(manifest)} text files for v29')

if __name__=='__main__':main()
