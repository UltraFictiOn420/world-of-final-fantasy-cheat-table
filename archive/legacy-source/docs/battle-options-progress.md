# Eight requested battle options — 2026-10-10

## v18 capture permission and buff repairs — latest work

Artifact: `outputs/World of Final Fantasy - Original v18.CT`. 22 structural/model tests pass.
Original sources updated; no GitHub publication requested/performed this turn.
Game PID13608, current CE26384. Both target windows found through computer-use skill.

After the user chose Defend, both stack actors16B51F60/16B89760 and all four member
actors16CD5380/16E122B0/16B5A3A0/16F04B20 acquired mask3600 (Haste/Regen/Protect/Shell).
Enemy Behemoth16F210F0 remained mask0. Party stack11338/11340 became11340/11340 without
an attack or healing-item request; this is consistent with native Regen healing.
Aggregate flags without member flags were confirmed BEFORE advancing time.

Status repair adds observed player/partner classes2F49E78/2F3DF30 to application/removal
guards, bounds stack member vectors to at most3 entries, and maintains Protect/Shell hit
counters alongside clocks when duration protection is enabled. Source uses unsigned counter
comparison to preserve negative infinite sentinels; the first live install still used signed
comparison for these two counters. Reinstall status only at a safe paused command menu or
load v18 to synchronize that minor correction. Do NOT rerun capture installer during capture.
UPDATE: status-only reinstall completed after capture, outside battle at save-complete screen.
Unsigned-counter final source now synchronized to live ID110; enable/disable/restoration
passed again (woff-status-final-v18-check.txt). All selections preserved.
Other battle behavior, negative-status blocking and later battle transitions need gameplay tests.

Easy Imprism extends four existing hooks with two independent permission hooks:
-241A88 native capture eligibility: bypass ONLY permission gate to241A9D for verified
 enemy Mirage class2F39FC0, side1, and species in248 library-listed installed definitions.
-55F898 native UI capture capability binding: same read-only predicate, preserving native
 setne/result construction. No whole-command override or fabricated Lua object.
Native living-target/capture-state/battle gates remain. No actor2B40 fields changed;
Behemoth permission remains0. Experimental/outside-library IDs and player IDs excluded.
Readiness/chance/Prism guards no longer require the original encounter permission bit.
No new permanent trace, timer, temp record or copied third-party code.
All six capture and two status hooks compiled, enabled, disabled, verified exact restored
instructions, then re-enabled preserving user's selections. Log:woff-repairs-v18-check.txt.
One-time Lua editor command cleared and editor closed. User asked to test capturing
Behemoth with replacement OFF and verify owned Mirage after battle; outcome pending.
UPDATE: user reports "Capture successful"; screenshot afterward confirms battle ended and
user saved in Sylver Park. Behemoth ownership/reload details not independently inspected.
Screenshot after repair shows selectable Imprism and Behemoth readiness effect.
Story encounter captures may affect progression: separate save recommended; no story-event
bypass, no forced completion, and no claim all bosses are capture-safe.

Current artifact: `outputs/World of Final Fantasy - Original v15.CT`.
Seven options implemented as TEST entries; Never Miss not implemented yet.
Do not claim all eight finished. No GitHub upload for these new experiments yet.

## Live check

Game PID22088, CE17832, build2.0.0.0 timestamp5B9B7E76.
Native status hook compiled/enabled. All five status child toggles enabled in
the user's existing CE table; previous working selections preserved.
User chose Defend once. Native calls counter8 and both active party stack actors
had status2AB0=3600: bits9/10/12/13 (Protect/Shell/Regen/Haste).
Both enemy Chocochicks retained status0. This proves scope/application, not all
effect behavior, expiry, immunity, or later battle stability. Separate party
individual actor retained0; native calls use stack status application without
propagating to members, matching native seven-argument call layout.

Critical and stack protection entries116/117 compiled, enabled, disabled and
native entry bytes checked afterward. They remain OFF for user testing.
The five status entries111..115 remain ON. Original GodMode and OneHitKill are ON.
They can mask Regen/Protect testing and damage comparisons.
Lua editor one-time commands must be cleared and window closed before handoff.

## Native anchors / implementation

- Status update236F40, RDI actor, R12D statusID/R13 index. Runs on game thread.
  Before native status test, apply missing selected statuses via actor virtual700
  with native args: actor, statusID,1,0,1,null,1.
  Preserve flags and every volatile integer and XMM0..5 register; x64 stack aligned.
- Native status setter23BDB0. Negative-status filter applies only to verified
  party classes, R8D nonzero, explicit IDs1..8,14,18,20,22,24,26,28.
  KO0, removal and enemies retain native behavior. Does not cure existing effects.
- Positive mask0AABB600:9,10,12,13,15,16,17,19,21,23,25,27.
  Native337C+ID*4 clocks kept>=1 for beneficial effects other than Regen.
  Regen3420 counter kept>=2; its clock still runs for healing ticks.
  Battle cleanup/removal is not intercepted. Effects wear off naturally when disabled.
- Critical chance native568780, binding getAutoAbilityCriticalPar(_impl).
  RCX wrapper+8 actor, positive native EDX chance only. Verified party returns100;
  zero/noncritical-capable attack and enemy retain native calculation. Gameplay
  and interpretation of100 as guaranteed percentage still need confirmation.
- Stack balance native setter55C782, RCX actor. Party stack class only, living,
  writes own native maximum2B2C into current2B28. Does not intercept manual unstack;
  direct forced-topple paths not yet proven covered. Getter55C7A0.

## Still pending: Never Miss

Combat scripting uses embedded Lua bindings; no loose .lua/.lbn files found.
Read-only `woff_lua_binding_probe.py` finds RIP references for named bindings.
Useful strings: AttackHitCheck, attackHitCheck, effectiveAttackHitCheck,
effectiveDexterity, getStatusParam, getTowerMemberStatusParam.
Ability-param Lua getters4A4763 ([RDI+18]) and4A5193 ([RDI+44]) are ability fields,
NOT party actors. Do not globally alter them: would help enemies too.
Need locate genuine hit decision with source actor guard; increasing dexterity
without proving hit calculation is not a verified Never Miss implementation.

Loot ID100 remains provisional. User reports modest Mu rewards (one Potion/Gil).
Do not promise rare loot or arbitrary items from the positive-drop roll bypass.
# v17 buff repair — gameplay test pending

User started a new game and reports buffs ineffective and Imprism greyed out on Behemoth.
Current game PID13608, CE14988. Enemy16F210F0 is normal Behemoth species1B83, HP8300,
native capture capability actor+2B40=0, Prism ID283. Native eligibility241A88 explicitly
returns false for capability0, before Prism and other gates. Our Easy Imprism keeps that
restriction. User says another table previously captured this enemy; that is consistent with
a capability override, not proof this instance is natively capturable. Capture repair/bypass
NOT implemented yet. Avoid claiming solved or forcing scripted battle completion.

Native stack setter231340 calls base23BDB0, then propagates to members only if its seventh
argument is0. v15/v16 incorrectly passed1. The new source passes0 and checks member statuses
at stack3690..3698 before treating the stack mask as complete. This repairs existing aggregate
flags with missing member effects. Native timer/duration behavior still needs gameplay tests.
Installed revised ID110 in current CE via woff_fix_status_v17.lua. Parent and111..115 selections
preserved, compile/activation passed. Generated v17, 21 structural tests passed. Needs user
Defend to let native update advance, then inspect member flags and actual effects; not yet
gameplay-confirmed. No GitHub update this turn.

# v16: Never Miss — current test

The user reported Always Critical works; its TEST tag is removed. Other status and balance behavior
remains pending gameplay verification.

Read-only Lua 5.1 prototype inspection located `AttackHitCheck_General` in
`@battle_attack_hit_check.lua`. Native getStatusParam at WOFF+558B10 copies
actor+2E34 into returned status+10, whose Lua property is playerType (getter WOFF+29A973).
0 is player-side; 1 is enemy-side. The general script uses a 0..100 random roll against
ability accuracy minus evasion plus attacker dexterity, halved for blind.

The new original implementation changes only the final six instructions (diagnostic logging and
returns) to read attacker:getStatusParam().playerType, replace the existing result with boolean true
for type 0, and return it. Type 1 preserves its existing boolean. Forced-miss, resurrection,
capture and other hit routines are not patched. Only K1 diagnostic text is replaced by the native
rooted playerType TString; the original diagnostic TString is also rooted by the other hit-check
prototypes. No extra game GC objects or prototype allocations are made.

Code/source/constant counts and content are validated, with unique prototype and property name
requirements. Disable checks the same process/prototype/pointers and exact patched bytes before
restoring. Destroyed VM memory is not written; retoggle in a battle if the VM was rebuilt.
Live CE enable/disable/re-enable checks passed, including all 24 original code bytes and the original
constant pointer restoration. Left ID118 enabled for the user's two-Mu battle. Gameplay pending.
Generated v16 table; 21 structural/model tests passed. No GitHub upload this turn.

# v19: F8 enemy topple test (2026-10-10)

User is in a battle with Mini Golem/Copper Gnome stack. PID13608, actor16B6FB70,
UnitTower vtable142F4B168, side1, HP341/341, balance150/150, two members at
16D8ECD0 (7068) and16D923B0 (7166). No HP/capture/ownership memory is changed.

Original new source `woff_topple_script.py` queues one F8 request in CE and consumes it
only inside the native actor update at WOFF+2379F6. Guards require a living enemy
UnitTower, two/three members, no disabled flag, and a live battle manager. It invokes
native onDamageTowerCollapse at55D440 using a local wrapper view with actor at+8.
That routine validates actor RTTI, identifies native manager slot, and queues the
native collapse action through1DA410. Never calls game routines on a CE worker thread.
Preserves flags, GPRs, XMM0..5 and provides aligned shadow space. Requests expire3s.

Earlier balance-getter55C7E4 and HUD-balance24CB70 hooks did not observe eligible enemies
at the command menu; both are restored to original bytes. Final actor hook remains
enabled as entry119; all preexisting selections were preserved. No collapse request
has been consumed yet: command menu pauses actor updates. Ask user to press F8 then
immediately choose Defend to advance battle time, and verify separation without HP loss.

Live compile/enable/disable/8-byte restoration/re-enable checks PASS. Request/Seen/Calls
addresses145150140/145150144/145150148, initially all0. Installer command cleared from
table Lua editor. Built v19 artifact,23 structural tests PASS. Gameplay pending; TEST
label retained. No GitHub actions this turn.
F8 was sent once through the game window: request changed to1, then automatically
expired back to0 with Seen/Calls still0. Hotkey and stale-request protection verified.

User subsequently confirmed successful topple of Mini Golem/Copper Gnome. Their
observed timing: press F8 and choose Defend just before the enemy's turn. This confirms
separation in this encounter, not all stacks or unchanged HP by user observation.
Saved v19 description removes TEST and explains the timing; comments retain the
other-encounters limitation. Native code unchanged. Live CE row not relabelled this
turn (still the installed working script); reload saved artifact only after disabling
old scripts, if desired. No GitHub update requested/performed.

## End-of-day GitHub backup completed

User requested all GitHub updates before a break. Current curated v19 package uploaded
through GitHub plugin; main commit2aa41045105f3410756141d9e953218fc045211a. All31
changed/new file Git blob hashes matched remote readback. v13-v18 retained in archive;
superseded outputs/v13 removed from current-output listing with archive/v13 preserved.
README, categorized feature catalogue, usage/testing, changelog, checksum and next-session
checkpoint updated. Rebuilt packaged source:23 table checks and4 catalogue checks pass.

Published v19 pre-release through the built-in in-app browser (no external browser).
https://github.com/UltraFictiOn420/world-of-final-fantasy-cheat-table/releases/tag/v19
Assets:WoFF-Original-v19.CT and matching CHECKSUMS.sha256. Published tag points to the
same main commit. GitHub's asset digest matches local table SHA256:
816c7a43f5376ca142bed4d49df052fa70bc2c57f449d157f058515f4a7dc3df.
Pre-release retained because broader status/accuracy/loot/replacement testing remains.
Screenshot:outputs/woff-v19-github-release.png. Repo stays private; launcher stays public.

All remote tracked files in the Actraiser, Asylum, City, Origins, Knight and launcher
repositories were compared against their existing local curated backups:155 files,
no differences or missing local copies. No changes were needed there. The deleted
research repository was NOT recreated. Game and CE were not operated this turn.

## 2026-10-11: v20 stack protection test and accuracy quarantine

User reports Never Miss possibly crashed the game; no causality confirmed. It was
inactive in the restarted process. Blocked live entry activation and replaced v20
release entry with a grey informational group header, preserving original source
for investigation. Do not re-enable the old v19 accuracy script.

Observed live party UnitTowers in PID10532: 1696F270 balance115/115 and
169868C0 balance12.819967/115. Never Topple117 initially inactive.
Extended original balance setter with guarded party-only native HUD and wobble
getter hooks, preserving registers/flags and restoring all original instructions
on disable. No cached actor pointers or cross-thread native calls. Installed live;
compile/enable/disable/re-enable checks passed. Wobble repair and resistance to
enemy attacks still require gameplay confirmation; reads immediately after window
focus continued to show12.82/115, so do not claim immediate repair verified.
v20 structural tests23/23 pass. One-time table Lua installer removed after use.
v19 artifact preserved from curated backup; no GitHub update this turn.

Outstanding requests: immediate buff application without Defend, cleaner F8 enemy
topple timing, controlled loot baseline vs cheat test, Never Miss crash diagnosis.


