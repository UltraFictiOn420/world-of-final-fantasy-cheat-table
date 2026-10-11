"""Curated source backup; never includes saves, game assets or memory dumps."""
from pathlib import Path
import json
import shutil
import hashlib
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT/'outputs/github-projects/world-of-final-fantasy-cheat-table'

def write(name, content):
    path = DEST/name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')

def main():
    for name in ('build_woff_table.py','woff_battle_scripts.py','woff_cost_item_scripts.py',
                 'woff_capture_scripts.py','woff_replacement_v9.py','woff_replacement_options.py',
                 'woff_save_script.py','woff_info_readonly.lua','woff_mirage_catalogue.py',
                 'woff_loot_scripts.py','woff_status_scripts.py','woff_combat_extra_scripts.py',
                 'woff_accuracy_script.py','woff_topple_script.py',
                 'test_woff_table.py','test_woff_catalogue.py','ue3_inspect.py'):
        (DEST/'work').mkdir(parents=True,exist_ok=True)
        shutil.copy2(ROOT/'work'/name, DEST/'work'/name)
    records=json.loads((ROOT/'work/woff-mirage-catalogue.json').read_text(encoding='utf-8'))
    cleaned=[{k:v for k,v in r.items() if k!='raw_cells'} for r in records]
    write('work/woff-mirage-catalogue.json',json.dumps(cleaned,ensure_ascii=False,indent=2)+'\n')
    latest=ROOT/'outputs/World of Final Fantasy - Original v21.CT'
    (DEST/'outputs').mkdir(exist_ok=True)
    shutil.copy2(latest,DEST/'outputs'/latest.name)
    for version in range(1,21):
        source=ROOT/'outputs'/f'World of Final Fantasy - Original v{version}.CT'
        if not source.is_file():
            continue
        (DEST/'archive').mkdir(exist_ok=True)
        shutil.copy2(source,DEST/'archive'/source.name)
    entries=E.parse(latest).findall('.//CheatEntry')
    def category(ident):
        if ident==1:return 'Foundation'
        if ident in (10,11,20,21):return 'Economy / Mirage Board'
        if ident in (30,31,32):return 'Progression'
        if ident in (40,41,42,50,51):return 'Battle survival'
        if ident in (43,44,45,116,118):return 'Battle offense'
        if ident in (60,61,62):return 'Costs / inventory'
        if ident==70:return 'Capture'
        if 80<=ident<=85:return 'Capture replacement'
        if ident==90:return 'Field utility'
        if ident==100:return 'Battle rewards'
        if 110<=ident<=115:return 'Party statuses'
        if ident in (117,119):return 'Battle stacks'
        return 'Other'
    def status(e):
        ident=int(e.findtext('ID'));desc=e.findtext('Description')
        if ident in (83,84,85):return 'read-only information'
        if ident==118:return 'unavailable; possible crash reported, causality unconfirmed'
        if ident==117:return 'provisionally user-confirmed; existing wobble clears on next action'
        if ident in (1,11,31,40,44,45,50,60,81):return 'supporting control / editable setting'
        if 80<=ident<=82:return 'experimental; two ownership replacements user-confirmed'
        if 'TEST' in desc:return 'implemented; further gameplay validation pending'
        if ident==70:return 'user-confirmed Mu, Chocochick, Behemoth; other encounters unverified'
        if ident==119:return 'user-confirmed Mini Golem/Copper Gnome; other stacks unverified'
        return 'user-confirmed within documented test scope'
    features=[{'id':int(e.findtext('ID')),'description':e.findtext('Description').strip('"'),
               'game':'World of Final Fantasy (Steam/PC)', 'category':category(int(e.findtext('ID'))),
               'code_type': 'Auto Assembler / Lua' if e.find('AssemblerScript') is not None else e.findtext('VariableType'),
               'status':status(e)} for e in entries]
    write('catalog/features.json',json.dumps(features,ensure_ascii=False,indent=2)+'\n')
    write('README.md', '''# World of Final Fantasy — Original Cheat Table

Steam/PC, developed with UltraFictiOn420 and AI assistance. Current version: **v21** (2026-10-11). This is an ongoing project, not a universally tested final release.

## Start here

Download [the current table](outputs/World%20of%20Final%20Fantasy%20-%20Original%20v19.CT), open it in Cheat Engine, attach to `WOFF.exe`, load your game, and enable the **Enable First** parent. Then enable only the features you need. Back up saves and use a separate slot for experimental changes. Disable child scripts before the parent and before closing Cheat Engine. Do not load two table versions together.

Latest highlights: Behemoth capture permission fixed; stacked-member buffs repaired; enemy stack topple added. **Topple: enable its entry, press F8, then immediately choose Defend just before the enemy's turn.** The command menu can pause the updates that process it. One enemy stack per press; requests expire after three seconds.

Verified executable: Windows x64 `WOFF.exe`, version 2.0.0.0, PE timestamp `5B9B7E76`. Other builds are not certified. The table checks this timestamp and hook bytes; a match is not a guarantee of universal compatibility.

## Feature categories and status

| Category | Included features | Status |
| --- | --- | --- |
| Economy / Mirage Board | Gil; ignore SP requirement; no SP deduction | User-tested |
| Progression | XP multiplier (0, 1, 50000 supported); max level on next positive XP | User-tested; results appear after battle on field |
| Battle survival | God Mode; always max HP/AP for living party; infinite AP | User-tested; not status immunity or revival |
| Battle damage | One-hit kill; player and enemy damage multipliers | User-tested |
| Costs / inventory | Zero ability AP cost; infinite item usage; never below one item | User-tested in battle and field; must own item |
| Capture | Easy Imprism with conditions/chance, Prism bypass and library-Mirage encounter permission | Mu, Chocochick and Behemoth captured; story caution; other native gates remain |
| Capture replacement | One-shot species dropdown; protected information rows | Experimental; Mu → Chocochick and Mu → Goblin ownership confirmed |
| Field utility | Save Anywhere through field menu | Saved and reloaded successfully; disable fixed in v12 |
| Battle critical | Always Critical | User-confirmed; critical-capable attacks only |
| Party statuses | Haste, Regen, Protect/Shell, positive-duration protection, block negative statuses | Revised native stack/member propagation verified in memory; broader gameplay tests pending |
| Battle accuracy | Never Miss | Unavailable informational row; possible crash reported, causality unconfirmed |
| Party stacks | Stacks Never Topple | Provisionally user-confirmed; existing wobble clears after next battle action |
| Enemy stacks | F8 Topple One Enemy Stack | User-confirmed Mini Golem/Copper Gnome; F8 then Defend before enemy turn |
| Battle rewards | Guaranteed Enemy Loot Rolls | TEST; positive-chance drops only; observed Mu loot not enough to establish broad effectiveness |
| Pending | Champion cost zero; richer loot/quantity options | Not implemented |

## Organized project map

- `outputs/`: current ready-to-use table.
- `work/`: current original builder, script modules, Lua guards, catalogue metadata and tests.
- `catalog/`: machine-readable feature index.
- `docs/`: usage, validation, development history and research scope.
- `archive/`: old snapshots, **not recommended for gameplay**; see archive warnings.
- `CHANGELOG.md`: version milestones.

The reference DrummerIX table was used for context, not redistributed. No game executable, packaged game assets, personal saves, credentials or raw memory dumps are included. The old research repository is not recreated. The [standard-user launcher](https://github.com/UltraFictiOn420/world-of-final-fantasy-launcher) remains a separate project.

## Development

Python 3: `python work/build_woff_table.py`, then `python work/test_woff_table.py`. The 23 structural/model checks require no game and do not enable cheats. Optional catalogue validation needs your installed game; optional live checks need Windows, `pefile`, and a clean unpatched process. `ue3_inspect.py` is a developer memory helper capable of writes; ordinary users do not need to run it. The packaged builder includes all current script-module dependencies.

See [usage and safety](docs/usage.md), [testing status](docs/testing.md), and [history](CHANGELOG.md). No warranty; use offline single-player only.
''')
    write('docs/usage.md','''# Usage and limitations

Enable the parent first. Grey INFO ONLY rows cannot be frozen or edited through ordinary table controls; dropdown selections and multipliers remain editable. No temporary trace or data-collection hook is shipped in the current table.

## XP and damage

XP appears after the fight when back on the field. XP multiplier 0 is none; 1 is normal; 50000 is supported. Max Level overrides the multiplier and needs a positive award. This is not a certified unlimited numeric range.

One-Hit Kill overrides player damage multiplier. God Mode / Always Max override enemy damage multiplier. Multipliers operate by target side, not attacker identity; healing and zero-damage hits are not multiplied. Always Max applies to living battle actors, does not revive KO actors, and may need retoggling if actors are rebuilt.

## Items and currency

Gil and refilled values remain after disabling. Item modes require an owned item; Infinite Usage takes priority over Never Below 1. Disable item options before selling, crafting or quest hand-ins; those paths are not validated.

## Capture replacement — experimental

Enable the section, choose a normal species, then arm ONE capture. It starts disarmed. Capture once and finish the battle without re-arming or disabling the section while status is queued. The animation and naming screens may still show the original species. **Verify the replacement in your Mirage list after fully leaving battle.** Toggle Arm off/on to re-arm for a later battle.

Only Mu → Chocochick and Mu → Goblin ownership are confirmed. The 264 candidates (248 library-listed) are metadata candidates, not a promise that all are safe or ownable. Unused/test/outside-library entries remain explicitly marked. Multiple captures in one battle, all species, abilities, boards and saved replacement persistence need broader testing. Status Idle/consumed alone does not prove success; check ownership and free slots.

Easy Imprism combines conditions/chance and capture-only Prism bypass. v18 also bypasses encounter capture permission ONLY for library-listed enemy Mirage species. Behemoth capture is user-confirmed. Living-target, capture-state and other battle checks remain. It does not promise all bosses or scripted encounters are safe: capturing a story opponent may affect progression. Use a separate save and verify your Mirage list afterward.

## F8 enemy topple

Enable Topple One Enemy Stack. In battle, press F8, then immediately choose Defend just before the enemy's turn. Command-menu wait mode may pause the required actor update. It queues the game's native collapse action, not an instant menu animation. One living enemy stack (two or three members) per press; repeated presses may be needed for multiple stacks. Pending requests expire after three seconds to avoid a stale press triggering in a later battle. No HP-damage, party-balance, capture or ownership writes are made by this script. Mini Golem/Copper Gnome separation is user-confirmed; HP preservation and other encounters need broader observation. Disable removes the hotkey and timer and restores the native update bytes.

## Battle statuses, accuracy and loot

Buffs need battle time to advance (choose Defend). v18 repairs propagation to stack members and includes observed Lann/Reynn actor classes. Party/enemy separation and member status flags were checked in live memory. These checks are not proof that every effect behaves correctly across later battles; TEST labels remain on status options. Negative-status protection does not revive KO or cure existing effects; duration protection excludes Reflect/Berserk.

Always Critical applies only to critical-capable party attacks. Never Miss is unavailable: a possible crash was reported, but causality has not been established. Its executable script is omitted from the current table; source is retained for investigation only. Party Stacks Never Topple protects balance, not manual unstack commands; the user provisionally confirmed protection, with existing wobble clearing after the next action.

Guaranteed Enemy Loot Rolls applies only to positive-chance eligible drops from defeated enemies, not captures. It does not invent rare items, multiply quantities or change quest rewards. A Mu yielded a potion and Gil, but broader effectiveness remains unconfirmed.

## Save Anywhere

Close and reopen the field menu after changing the toggle. It only removes the field Save entry's permission requirement; no automatic saving, battle/cutscene menus, save-file edits or persistent story flags. Use a separate save slot. Other maps/story states remain untested. Disable restores the original requirement.
''')
    write('docs/testing.md','''# Validation record — 2026-10-10

23 structural/model tests pass on v19. They check XML/IDs, hook restoration and scope, information-row protections, replacement queue/native grant boundaries, save-toggle address resolution, party-status scope/member propagation, accuracy bytecode boundaries, and enemy topple one-shot dispatch. Four installed-catalogue checks also pass. This is not equivalent to testing every game situation.

User gameplay confirmations: Gil/SP/XP, God Mode/AP, damage and max vitals, zero ability AP cost, both item modes, easy Mu/Chocochick/Behemoth capture, Mu-to-Chocochick and Mu-to-Goblin owned replacement, field saving and reloading, Always Critical, and F8 topple of Mini Golem/Copper Gnome.

v18 status evidence: after Defend, both party stacks and all observed members acquired Haste/Regen/Protect/Shell flags; enemy flags remained unchanged. Native Protect/Shell counters and propagation guards were repaired. Across-battle effects and negative-status protection still need player testing. Native capture hooks and status hooks passed compilation, enable/disable and exact-byte restoration checks.

v19 topple evidence: compile/enable/disable/native-byte-restoration/re-enable passed; F8 queues a one-shot request and unused requests expire. User confirmed separation after F8 then Defend just before the enemy turn. This does not independently confirm HP preservation or every enemy stack.

Save toggle was additionally compiled and exercised off/on/off successfully after the v12 disable-resolution repair. The inactive developer owned-Mirage trace was removed from the live session and is absent from the current artifact.

Remaining tests: champions/cost-zero implementation, broader enemy-stack/topple and party balance protection, buff behavior across battles, Never Miss, broader loot rolls and future quantity work, broader replacement catalogue and multi-capture, replacement board/ability/save persistence, other save-menu map/story states and non-use inventory removal. These are not marked completed.

v13 changed presentation/provenance and packaging only. v14-v19 add battle features and repairs. Archives include known failed versions for recovery/history, not use; use v19 rather than earlier buff/capture implementations.
''')
    write('docs/research.md','''# Research scope and provenance

Current implementation was built from independently inspected native routines. Capture replacement queues a successful eligible capture and substitutes the species argument at native owned-Mirage construction. It does not overwrite the source enemy species or existing owned Mirages. The failed visual-only v8 route is not imported by the current builder.

The Mirage catalogue was decoded independently from installed CSH definitions. Only identifiers, labels and classification metadata are included here; raw cell matrices and game assets are excluded. Library presence is classification, not proof of safe ownership.

Save Anywhere changes only the field-menu Save descriptor's required permission value to the native unrestricted sentinel and restores it when disabled. No save-writing routines or persistent event flags are patched.

Developer observation traces were disposable, inactive diagnostics, not cheats. They are excluded from the current table and published source. Personal save data, machine-specific logs and raw memory dumps stay local.
''')
    write('CHANGELOG.md','''# Version history

| Version | Milestone / caution |
| --- | --- |
| v1–v2 | Foundation, Gil/SP and XP options; enable-parent and compatibility work |
| v3 | God Mode and infinite battle AP |
| v4 | Damage options and always-max living party vitals |
| v5 | Zero ability AP cost and item-use modes |
| v6 | Easy Mu capture; Prism requirement still remained |
| v7 | Capture-only Prism bypass merged into Easy Imprism; Chocochick tested |
| v8 | Failed replacement prototype: visuals changed, ownership did not; DO NOT USE |
| v9 | Native owned-grant replacement; Mu → Chocochick confirmed |
| v10 | UI cleanup and protected informational rows |
| v11 | Field Save Anywhere; disable-time bug later fixed; DO NOT USE |
| v12 | Save disable resolution repaired; off/on/off checked; Goblin replacement confirmed |
| v13 | Clean current snapshot, updated validation notes, trace-free source backup and organized repository; gameplay hooks unchanged |
| v14 | Experimental positive-chance defeated-enemy loot-roll override; no quantity multiplier |
| v15 | Party buffs/status options, Always Critical and party stack-balance protection |
| v16 | Reversible party-only normal-accuracy override; gameplay testing pending |
| v17 | Initial stacked-member buff propagation repair; superseded by v18 |
| v18 | Scoped native/UI encounter capture permission for library Mirages; Behemoth captured; member status propagation/classes and Protect/Shell duration counters repaired |
| v19 | Original game-thread one-shot enemy topple, F8 then Defend before enemy turn; Mini Golem/Copper Gnome confirmed; clearer usage notes |

Old versions are archival snapshots only. Use v19. The capture catalogue and TEST-labelled features remain experimental; pending features are not promoted to completed.
''')
    write('archive/README.md','# Historical snapshots — not for gameplay\n\nUse v19 in outputs. Old tables may contain developer diagnostics, obsolete hooks and known bugs. v8 replacement failed to change owned species; v11 Save Anywhere could not disable normally; pre-v18 buffs and encounter capture permissions were incomplete. These snapshots are retained only to protect development history. Never enable multiple table versions together.\n')
    write('docs/next-session.md','''# Resume checkpoint — 2026-10-10

Current table: v19. Latest confirmed test: enemy Mini Golem/Copper Gnome topple using F8 then Defend just before the enemy turn. No changes to previously working battle scripts were made for topple.

Next priorities, chosen with the player:

- Verify revised buffs by observable effects across fresh battles; TEST labels remain.
- Verify Never Miss and party stack-balance protection separately.
- Try F8 on other ordinary two/three-member enemy stacks and observe HP preservation.
- Test loot against enemies with more varied drops before considering bounded quantities.
- Implement champion cost zero once a usable champion situation is available.
- Expand replacement ownership/board/ability/save-persistence tests using separate saves.

Do not enable multiple table versions together. Back up saves before risky story captures or unusual Mirage replacements. The deleted research repository stays deleted; launcher and cheat-table projects stay separate. No saves, machine-specific traces, raw memory dumps or game assets are included in this backup.
''')
    write('.gitignore','__pycache__/\n*.pyc\npydeps/\nprivate-backups/\nsaves/\n*.dmp\n*.log\n.env\n')
    write('requirements-dev.txt','pefile\n# Only optional Windows live checks need this dependency.\n')
    digest=hashlib.sha256(latest.read_bytes()).hexdigest()
    write('CHECKSUMS.sha256',f'{digest}  outputs/{latest.name}\n')
    # Refresh references in generated documents, without rewriting archived tables.
    for rel in ('README.md','archive/README.md','docs/testing.md','docs/next-session.md','CHANGELOG.md'):
        path=DEST/rel
        content=path.read_text(encoding='utf-8')
        content=content.replace('Original%20v19.CT','Original%20v21.CT')
        content=content.replace('Use v19','Use v21').replace('use v19','use v21')
        content=content.replace('Current table: v19.','Current table: v21.')
        content=content.replace('23 structural/model tests pass on v19.','23 structural/model tests pass on v21.')
        if rel=='CHANGELOG.md':
            content=content.replace('\nOld versions are archival', '\n| v20 | Scoped HUD/wobble balance repair; Never Miss quarantined following an unconfirmed crash report |\n| v21 | F8 accepted-request beep and explicit three-second expiry notes; Never Topple provisional user confirmation; status cleanup |\n\nOld versions are archival')
        if rel=='docs/next-session.md':
            content=content.replace('Verify Never Miss and party stack-balance protection separately.', 'Never Miss stays unavailable; investigate only if proportionate effort. Stack protection provisionally confirmed; existing wobble clears on next action.')
        write(rel,content)
    additions='''\n## v21 checkpoint — 2026-10-11\n\nF8 accepted-request beep is implemented using Cheat Engine's documented beep function; sound playback is not yet user-tested. It acknowledges queuing only. An unused request expires after three real-time seconds, including time spent in the command menu; it does not persist until the enemy turn. Defend is a convenient way to resume battle updates, not a required native collapse command. Do not press several turns early expecting a persistent request.\n\nNever Topple is provisionally user-confirmed: existing wobble animation cleared after Defend. Immediate menu-time repair remains unconfirmed. Buffs still require battle updates; immediate battle-start application is the next research priority, not an implemented fix. Loot effectiveness remains unconfirmed; positive-chance existing drops only, no invented items or quantity multiplier. Champion cost zero is not implemented and awaits a usable Champion. Replacement catalogue contains candidates, not universal ownership validation. Never Miss is a grey unavailable informational row, not a usable cheat; possible crash causality remains unconfirmed.\n'''
    for rel in ('README.md','docs/usage.md','docs/testing.md','docs/next-session.md'):
        write(rel,(DEST/rel).read_text(encoding='utf-8')+additions)
    def publishable(p):
        rel=p.relative_to(DEST)
        if not p.is_file() or '__pycache__' in rel.parts:return False
        if rel.parts[0]=='outputs' and p.name!=latest.name:return False
        return p.suffix.lower() in ('.md','.py','.lua','.json','.ct','.aa','.sha256') or p.name in ('.gitignore','requirements-dev.txt')
    manifest=[{'path':p.relative_to(DEST).as_posix(),'mode':'100644','type':'blob','content':p.read_text(encoding='utf-8')} for p in sorted(DEST.rglob('*')) if publishable(p)]
    (ROOT/'work/woff-github-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False),encoding='utf-8')
    print(f'Curated {len(manifest)} text files at {DEST}')

if __name__=='__main__':
    main()

