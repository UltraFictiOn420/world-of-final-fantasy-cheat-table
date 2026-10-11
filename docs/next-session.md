# Resume checkpoint — 2026-10-10

Current table: v21. Latest confirmed test: enemy Mini Golem/Copper Gnome topple using F8 then Defend just before the enemy turn. No changes to previously working battle scripts were made for topple.

Next priorities, chosen with the player:

- Verify revised buffs by observable effects across fresh battles; TEST labels remain.
- Never Miss stays unavailable; investigate only if proportionate effort. Stack protection provisionally confirmed; existing wobble clears on next action.
- Try F8 on other ordinary two/three-member enemy stacks and observe HP preservation.
- Test loot against enemies with more varied drops before considering bounded quantities.
- Implement champion cost zero once a usable champion situation is available.
- Expand replacement ownership/board/ability/save-persistence tests using separate saves.

Do not enable multiple table versions together. Back up saves before risky story captures or unusual Mirage replacements. The deleted research repository stays deleted; launcher and cheat-table projects stay separate. No saves, machine-specific traces, raw memory dumps or game assets are included in this backup.

## v21 checkpoint — 2026-10-11

F8 accepted-request beep is implemented using Cheat Engine's documented beep function; sound playback is not yet user-tested. It acknowledges queuing only. An unused request expires after three real-time seconds, including time spent in the command menu; it does not persist until the enemy turn. Defend is a convenient way to resume battle updates, not a required native collapse command. Do not press several turns early expecting a persistent request.

Never Topple is provisionally user-confirmed: existing wobble animation cleared after Defend. Immediate menu-time repair remains unconfirmed. Buffs still require battle updates; immediate battle-start application is the next research priority, not an implemented fix. Loot effectiveness remains unconfirmed; positive-chance existing drops only, no invented items or quantity multiplier. Champion cost zero is not implemented and awaits a usable Champion. Replacement catalogue contains candidates, not universal ownership validation. Never Miss is a grey unavailable informational row, not a usable cheat; possible crash causality remains unconfirmed.
