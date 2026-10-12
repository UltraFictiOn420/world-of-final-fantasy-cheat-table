# World of Final Fantasy — Original v30

Capture replacement now supports multiple Mirages in one battle, with a different replacement selected for each capture. Other gameplay scripts are unchanged from v29.

## Capture replacement

1. Before the first capture, enable the Capture Replacement parent.
2. Choose a replacement in the dropdown and enable **2. Leave this on while you wish to replace Mirage replacements**.
3. Imprism normally. To receive a different Mirage next, change the dropdown **before** the next Imprism. Earlier captures retain their own selections.
4. Keep the parent enabled through the entire battle and **all** confirmation/naming screens.
5. Once back in the **field**, disable and re-enable the parent before another capture battle. Choose a replacement and arm it again. This version does not automatically reset between battles.

Have enough free Mirage spaces for every intended capture. Use a separate save slot while testing unfamiliar replacements. Replacement does not itself unlock Imprism; use Easy Imprism when needed.

## Verified in gameplay

- Three Mandragoras became three Chocochicks, including correct capture visuals, confirmations, default names, ownership, and save/reload.
- Changing selection between three captures produced Chocochick, Mu, and Mini Golem. Visuals, confirmations, default names, ownership, and save/reload were correct.
- In a mixed-enemy battle, Copper Gnome became Chocochick and Floating Eye became Mu. Visuals, confirmations, default names, and ownership were correct. A defeated enemy did not interfere with the capture list.
- Fixed rejection of successful Easy Imprism captures whose original capture-permission flag was still zero.

## Limits and safety

- One capture battle per parent enable; reset only after all results are finished.
- Full storage, cancelled capture flows, and save/reload of the mixed-source pair have not been tested.
- Unusual/hidden replacements retain their warning labels. A listed species is not a guarantee of safe replacement.
- If the recorded captures do not match the native results list, the script leaves result IDs unchanged. Earlier animations may nevertheless have shown replacement appearances; check the owned list.
- Champion costs remain unverified until tested with an available champion. Other existing cautions remain in the table.

Grey INFO rows are read-only, not toggles. Diagnostic hooks and temporary trace entries are absent from the release file. v29 is preserved as a fallback.

For Save Anywhere, reopen the field menu after toggling the script. The shorter table descriptions do not remove the safety instructions above.

Before switching from a running older table, finish the battle/results and disable its cheats in the field. Load v30 and re-enable your desired cheats normally. Do not switch tables mid-capture or mid-naming.
