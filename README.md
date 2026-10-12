# World of Final Fantasy — Original Cheat Table

Steam/PC, developed with UltraFictiOn420 and AI assistance. Current snapshot: **v30**, 2026-10-12.
Ongoing project, not a universally tested final release.

## Download and start

[Download v30 from the repository](https://github.com/UltraFictiOn420/world-of-final-fantasy-cheat-table/raw/refs/heads/main/outputs/World%20of%20Final%20Fantasy%20-%20Original%20v30.CT).
The existing v29 release remains available as a fallback.
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
| Capture | Easy Imprism including Prism/permission bypass; multiple replacements per battle; selection stored per capture; species-size-status dropdown |
| Saving | Field Save Anywhere; reopen menu; separate save recommended |
| Unavailable | Never Miss: no active patch, possible crash causality unconfirmed |

Chocochick, Mu and Mini Golem replacements were confirmed through capture visuals, naming, ownership and save/reload. Copper Gnome → Chocochick and Floating Eye → Mu were also confirmed in one mixed-enemy battle (that pair has not had a save/reload check).
Change the dropdown before each Imprism to choose a different replacement. Keep the parent enabled through every result screen. **Reset the parent in the field between capture battles.** Full storage, cancelled captures and untested species remain unverified.
Dropdown ownership classification is partial; unknown/hidden/test/unused entries are not certified safe.
F8 beep means queued, not completed; queue expires in three real seconds. Press before Defend/enemy turn.
Never Topple may leave wobble animation until the next action. Champion cost behavior remains unverified without an available champion.

## Organization and development

- `outputs/`: current v30 table and preserved v29 fallback; `archive/`: historical snapshots, not recommended for play.
- `work/`: original source modules, builder, tests and curated catalogue metadata.
- `catalog/`: feature index; `docs/`: usage, testing, provenance and next steps.

45 local automated checks pass: 24 stable v29/model checks, 8 catalogue checks, 9 multi-capture checks and 4 v30 structure/description checks. Static/model checks are not universal gameplay proof.
Build the v29 baseline with `python work/build_woff_table.py`, then build v30 with `python work/build_woff_v30_preview.py --release`.
Run `python -m unittest discover -s work -p "test_woff*.py"`. Catalogue tests additionally need installed game data. Optional live checks require Windows/pefile.
The developer memory helper can write memory; ordinary users do not need to run it.
The clean v30 file preserves unrelated v29 cheats and the read-only information guard. Live gameplay testing used the instrumented equivalent of the replacement hooks; clean-file checks cover structure and preservation.

No game binaries/assets, saves, raw memory dumps, credentials or machine-specific installers are included.
Reference tables were studied for context; their scripts are not redistributed. Deleted research repo stays deleted.
[Launcher project](https://github.com/UltraFictiOn420/world-of-final-fantasy-launcher) remains separate.
See [usage](docs/usage.md), [testing](docs/testing.md), [next steps](docs/next-session.md), [history](CHANGELOG.md).
Offline single-player only; no warranty. v30 is backed up on the main branch; the Releases page still contains the previous v29 release. See [v30 notes](docs/v30-release-notes.md) for capture instructions and limits.
