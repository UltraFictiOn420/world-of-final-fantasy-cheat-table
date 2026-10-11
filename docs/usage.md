# Current usage — v29

World of Final Fantasy - Original v29. UI/documentation cleanup; game hooks unchanged from v28.

START: Attach CE to WOFF.exe, load a save, then enable the top entry. Section folders organize the table; they are not cheat scripts. Enable feature parents before their child options. Disable cheats before closing CE or loading a different table.

XP: Results become visible after battle on the field. 0 = none, 1 = normal; 50000x supported. Max Level overrides the multiplier for positive XP awards.
DAMAGE/AP: One-Hit Kill overrides the player multiplier. God Mode blocks HP damage, not statuses. Always Max applies to living party members, does not revive KO, and may need retoggling if actors rebuild.
ITEMS: Infinite Usage overrides Never Below 1. You must own the item. Disable for selling, crafting and quest hand-ins until those removal paths are verified. Loot uses native quantities and does not multiply Gil.
BUFFS: Selected Haste/Regen/Protect/Shell apply before the first action; fresh-battle visuals were user-confirmed. Duration protection and negative-status blocking remain unverified.
STACKS: Never Topple may leave the wobble animation until the next action. F8 queues ONE enemy stack topple; beep confirms queuing, not completion. Queue expires after three real seconds. Press just before Defend/enemy turn and resume battle promptly.

CAPTURE: Easy Imprism includes readiness/chance/prism bypass and permission for library-listed Mirages. Story captures can affect progression; use a separate save. Replacement: enable parent, select species, arm once, capture ONE Mirage, and finish battle without disabling/re-arming. Toggle Arm off/on for the next battle. Chocochick capture animation, naming model/default name and owned species were user-confirmed with v27. Other replacement species and save/reload safety are not comprehensively validated.
DROPDOWN: Name [Size] - ownership status. LL/EX display XL; EX summons are explicitly marked. Legit means normally obtainable, not guaranteed safe under replacement. Classification is partial. Library membership alone does not prove ownability. Hidden/test/unused entries remain unverified, not certified safe or known save-breaking. Grey INFO ONLY rows cannot be frozen/edited through ordinary controls; selectors and multipliers remain editable.

SAVE: Field menu only; close/reopen the menu after toggling. Separate save slot recommended. Gil, XP, owned Mirages and other already-applied persistent results are not undone by disabling.
UNAVAILABLE: Never Miss has no active patch following a possible crash report. Champion cost is not implemented. No temporary traces or auto-running table Lua are included.
Original scripts; third-party tables were reference context only. Build guard targets the verified WOFF executable. Broader encounter/DLC compatibility still needs testing.
