# Validation — v29, 2026-10-11

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

## v30 — 2026-10-12

45 automated checks pass (24 stable, 8 catalogue, 9 multi-capture and 4 v30 checks). The release file preserves every unrelated v29 gameplay script and all dropdown entries. Its XML contains no diagnostics or auto-run table Lua.

Live instrumented replacement tests: three Mandragoras to three Chocochicks, correct visuals/naming/ownership/boards and save/reload; another three-Mandragora battle to Chocochick/Mu/Mini Golem with dropdown changes, correct visuals/naming/ownership and save/reload. The mixed replacement batch's boards were not explicitly reported.

Mixed-source battle: one Copper Gnome was defeated; another was replaced with Chocochick and Floating Eye with Mu. Both had correct animations, result/naming screens and ownership. Mixed-source save/reload remains pending. Successful Easy Imprism captures with native permission=0 are no longer rejected by the replacement filter.

One battle per parent enable; manually reset in field after all result screens. Full storage, cancellation and untested species remain unverified. Instrumented live checks do not replace a fresh clean-file gameplay test on other builds.
