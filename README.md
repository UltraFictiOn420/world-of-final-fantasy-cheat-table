# World of Final Fantasy — Original Cheat Table

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
