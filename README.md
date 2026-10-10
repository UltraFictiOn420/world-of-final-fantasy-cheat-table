# World of Final Fantasy — Original Cheat Table

Steam/PC, developed with UltraFictiOn420 and AI assistance. Current version: **v13** (2026-10-10). This is an ongoing project, not a universally tested final release.

## Start here

Download [the current table](outputs/World%20of%20Final%20Fantasy%20-%20Original%20v13.CT), open it in Cheat Engine, attach to `WOFF.exe`, load your game, and enable the **Enable First** parent. Then enable only the features you need. Back up saves and use a separate slot for experimental changes. Disable child scripts before the parent and before closing Cheat Engine.

Verified executable: Windows x64 `WOFF.exe`, version 2.0.0.0, PE timestamp `5B9B7E76`. Other builds are not certified. The table checks this timestamp and hook bytes; a match is not a guarantee of universal compatibility.

## Feature categories and status

| Category | Included features | Status |
| --- | --- | --- |
| Economy / Mirage Board | Gil; ignore SP requirement; no SP deduction | User-tested |
| Progression | XP multiplier (0, 1, 50000 supported); max level on next positive XP | User-tested; results appear after battle on field |
| Battle survival | God Mode; always max HP/AP for living party; infinite AP | User-tested; not status immunity or revival |
| Battle damage | One-hit kill; player and enemy damage multipliers | User-tested |
| Costs / inventory | Zero ability AP cost; infinite item usage; never below one item | User-tested in battle and field; must own item |
| Capture | Easy Imprism with condition/chance and Prism bypass | Mu and Chocochick tested; native eligibility remains |
| Capture replacement | One-shot species dropdown; protected information rows | Experimental; Mu → Chocochick and Mu → Goblin ownership confirmed |
| Field utility | Save Anywhere through field menu | Saved and reloaded successfully; disable fixed in v12 |
| Pending | Champion cost zero; instant enemy unstack | Not implemented; appropriate test situations still needed |

## Organized project map

- `outputs/`: current ready-to-use table.
- `work/`: current original builder, script modules, Lua guards, catalogue metadata and tests.
- `catalog/`: machine-readable feature index.
- `docs/`: usage, validation, development history and research scope.
- `archive/`: old snapshots, **not recommended for gameplay**; see archive warnings.
- `CHANGELOG.md`: version milestones.

The reference DrummerIX table was used for context, not redistributed. No game executable, packaged game assets, personal saves, credentials or raw memory dumps are included. The old research repository is not recreated. The [standard-user launcher](https://github.com/UltraFictiOn420/world-of-final-fantasy-launcher) remains a separate project.

## Development

Python 3: `python work/build_woff_table.py`, then `python work/test_woff_table.py`. The 17 structural checks require no game and do not enable cheats. Optional catalogue validation needs your installed game; optional live checks need Windows, `pefile`, and a clean unpatched process. `ue3_inspect.py` is a developer memory helper capable of writes; ordinary users do not need to run it.

See [usage and safety](docs/usage.md), [testing status](docs/testing.md), and [history](CHANGELOG.md). No warranty; use offline single-player only.
