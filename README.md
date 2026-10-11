# World of Final Fantasy — Original Cheat Table

Steam/PC, developed with UltraFictiOn420 and AI assistance. Current version: **v21** (2026-10-11). This is an ongoing project, not a universally tested final release.

## Start here

Download [the current table](outputs/World%20of%20Final%20Fantasy%20-%20Original%20v21.CT), open it in Cheat Engine, attach to `WOFF.exe`, load your game, and enable the **Enable First** parent. Then enable only the features you need. Back up saves and use a separate slot for experimental changes. Disable child scripts before the parent and before closing Cheat Engine. Do not load two table versions together.

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

## v21 checkpoint — 2026-10-11

F8 accepted-request beep is implemented using Cheat Engine's documented beep function; sound playback is not yet user-tested. It acknowledges queuing only. An unused request expires after three real-time seconds, including time spent in the command menu; it does not persist until the enemy turn. Defend is a convenient way to resume battle updates, not a required native collapse command. Do not press several turns early expecting a persistent request.

Never Topple is provisionally user-confirmed: existing wobble animation cleared after Defend. Immediate menu-time repair remains unconfirmed. Buffs still require battle updates; immediate battle-start application is the next research priority, not an implemented fix. Loot effectiveness remains unconfirmed; positive-chance existing drops only, no invented items or quantity multiplier. Champion cost zero is not implemented and awaits a usable Champion. Replacement catalogue contains candidates, not universal ownership validation. Never Miss is a grey unavailable informational row, not a usable cheat; possible crash causality remains unconfirmed.
