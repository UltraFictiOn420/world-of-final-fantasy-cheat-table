# Usage and limitations

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

## v21 checkpoint — 2026-10-11

F8 accepted-request beep is implemented using Cheat Engine's documented beep function; sound playback is not yet user-tested. It acknowledges queuing only. An unused request expires after three real-time seconds, including time spent in the command menu; it does not persist until the enemy turn. Defend is a convenient way to resume battle updates, not a required native collapse command. Do not press several turns early expecting a persistent request.

Never Topple is provisionally user-confirmed: existing wobble animation cleared after Defend. Immediate menu-time repair remains unconfirmed. Buffs still require battle updates; immediate battle-start application is the next research priority, not an implemented fix. Loot effectiveness remains unconfirmed; positive-chance existing drops only, no invented items or quantity multiplier. Champion cost zero is not implemented and awaits a usable Champion. Replacement catalogue contains candidates, not universal ownership validation. Never Miss is a grey unavailable informational row, not a usable cheat; possible crash causality remains unconfirmed.
