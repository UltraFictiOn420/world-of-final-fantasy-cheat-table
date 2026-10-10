"""Original WoFF foundation table. No third-party CT or code is redistributed."""
from pathlib import Path
import xml.etree.ElementTree as E
from woff_battle_scripts import HP, MAX_VITALS, ap_script
from woff_cost_item_scripts import ZERO_AP, item_script
from woff_capture_scripts import easy_capture_script
from woff_replacement_v9 import replacement_script, dropdown as mirage_dropdown, ARM
from woff_save_script import SAVE
from woff_loot_scripts import LOOT
from woff_status_scripts import STATUS
from woff_combat_extra_scripts import CRITICAL, STACK
from woff_accuracy_script import ACCURACY
from woff_topple_script import topple_script

ROOT = Path(__file__).resolve().parents[1]

BOARD = r'''[ENABLE]
{$lua}
if syntaxcheck then return end
-- Never reopen the process inside AA: it can invalidate AA's captured handle.
if getOpenedProcessID()~=getProcessIDFromProcessName('WOFF.exe') then
  error('Select WOFF.exe in Cheat Engine before enabling the table.')
end
local b=getAddressSafe('WOFF.exe')
if not b then error('Start WoFF and load a save first.') end
local pe=readInteger(b+0x3C)
if not pe or readInteger(b+pe+8)~=0x5B9B7E76 then
  error('Unverified WoFF executable build; no patches applied.')
end
{$asm}
// Cost-availability check and spending are independent, but share our flags.
aobscanmodule(WFF_SPCheck,WOFF.exe,0F B7 80 E8 00 00 00 3B C3 0F 93 C0 48 83 C4 20 5B C3 CC)
aobscanmodule(WFF_SPCheckBase,WOFF.exe,0F B7 80 E8 00 00 00 3B C3 0F 93 C0 48 83 C4 20 5B C3 48 83 FA 03)
aobscanmodule(WFF_SPSpend,WOFF.exe,0F B7 81 E8 00 00 00 3B C3 72 2B 66 2B C3 66 01 99 EA 00 00 00)
assert(WFF_SPCheck,0F B7 80 E8 00 00 00 3B C3 0F 93 C0 48 83 C4 20)
assert(WFF_SPCheckBase,0F B7 80 E8 00 00 00 3B C3 0F 93 C0 48 83 C4 20)
assert(WFF_SPSpend,0F B7 81 E8 00 00 00 3B C3 72 2B 66 2B C3)
alloc(WFF_BoardCode,512,WFF_SPCheck)
label(WFF_CFG)
label(WFF_Availability)
label(WFF_AvailabilityBase)
label(WFF_EvaluateSP)
label(WFF_AvailabilityDone)
label(WFF_Spending)
label(WFF_ApplyCost)
label(WFF_KeepSP)
label(WFF_PaySP)
label(WFF_SPFailure)
registersymbol(WFF_CFG)
registersymbol(WFF_SPCheck)
registersymbol(WFF_SPCheckBase)
registersymbol(WFF_SPSpend)

WFF_BoardCode:
WFF_CFG:
db 00 00
align 10
WFF_Availability:
call WFF_EvaluateSP
add rsp,20
jmp WFF_SPCheck+10
WFF_AvailabilityBase:
call WFF_EvaluateSP
add rsp,20
jmp WFF_SPCheckBase+10
WFF_EvaluateSP:
// Preserve the original comparison result before consulting our option.
setae al
pushfq
cmp byte ptr [WFF_CFG],0
je WFF_AvailabilityDone
mov al,1
WFF_AvailabilityDone:
popfq
ret

WFF_Spending:
cmp byte ptr [WFF_CFG],0
jne WFF_ApplyCost
// Recreate the original affordability comparison when Ignore SP is disabled.
cmp eax,ebx
jb WFF_SPFailure
WFF_ApplyCost:
cmp byte ptr [WFF_CFG+1],0
jne WFF_KeepSP
cmp eax,ebx
jae WFF_PaySP
// Ignore SP never lets a 16-bit point balance wrap below zero.
xor eax,eax
jmp WFF_KeepSP
WFF_PaySP:
sub ax,bx
WFF_KeepSP:
jmp WFF_SPSpend+E
WFF_SPFailure:
jmp WFF_SPSpend+36

WFF_SPCheck+9:
jmp WFF_Availability
nop 2
WFF_SPCheckBase+9:
jmp WFF_AvailabilityBase
nop 2
WFF_SPSpend+9:
jmp WFF_Spending

[DISABLE]
WFF_SPCheck+9:
db 0F 93 C0 48 83 C4 20
WFF_SPCheckBase+9:
db 0F 93 C0 48 83 C4 20
WFF_SPSpend+9:
db 72 2B 66 2B C3
unregistersymbol(WFF_CFG)
unregistersymbol(WFF_SPCheck)
unregistersymbol(WFF_SPCheckBase)
unregistersymbol(WFF_SPSpend)
dealloc(WFF_BoardCode)
'''

GIL = r'''[ENABLE]
{$lua}
if syntaxcheck then return end
if WFF_GilTimer then error('Gil hold is already active.') end
local b=getAddressSafe('WOFF.exe')
if not b then error('Enable the table first.') end
local pid=getOpenedProcessID()
local function gilAddress()
  if getOpenedProcessID()~=pid then return nil end
  local root=readQword(b+0x3439EC0)
  if not root or root<0x10000 or root>=0x7FFFFFFFFFFF then return nil end
  local a=root+0x37368
  local v=readInteger(a)
  if not v or v<0 or v>9999999 then return nil end
  return a
end
if not gilAddress() then error('Gil data unavailable. Load your save first.') end
WFF_GilTimer=createTimer(nil,false)
WFF_GilTimer.Interval=100
WFF_GilTimer.OnTimer=function()
  local a=gilAddress()
  if a then writeInteger(a,9999999) end
end
WFF_GilTimer.Enabled=true
{$asm}
[DISABLE]
{$lua}
if syntaxcheck then return end
if WFF_GilTimer then
  WFF_GilTimer.Enabled=false
  WFF_GilTimer.destroy()
  WFF_GilTimer=nil
end
{$asm}
'''

XP = r'''[ENABLE]
aobscanmodule(WFF_XPGain,WOFF.exe,41 03 F0 3B C6 0F 42 F0 48 81 C1 98 00 00 00 E8 ?? ?? ?? ?? 48 8B 0D)
assert(WFF_XPGain,41 03 F0 3B C6)
alloc(WFF_XPCode,512,WFF_XPGain)
label(WFF_XPFactor)
label(WFF_XPMaxLevel)
label(WFF_XPOriginal)
label(WFF_XPReturn)
label(WFF_XPScaled)
label(WFF_XPClamp)
label(WFF_XPZero)
label(WFF_XPSetCap)
registersymbol(WFF_XPFactor)
registersymbol(WFF_XPMaxLevel)
registersymbol(WFF_XPGain)

WFF_XPCode:
// Here EAX is this recipient's level-99 total; R8D is current total XP.
// ESI is the recipient-specific award, after any upstream XP sharing.
test esi,esi
js WFF_XPOriginal
push r9
sub rsp,10
movups [rsp],xmm0
test esi,esi
jz WFF_XPZero
cmp byte ptr [WFF_XPMaxLevel],0
jne WFF_XPSetCap
// A 64-bit double intermediate avoids wrapping the 32-bit cumulative total.
mov r9d,esi
cvtsi2sd xmm0,r9
// Factor is Double: 0 = none, 1 = normal, 50000 = fifty thousand times.
mulsd xmm0,[WFF_XPFactor]
ucomisd xmm0,xmm0
jp WFF_XPScaled
mov r9d,eax
sub r9d,r8d
// At/past cap, leave the existing native cap check in control.
cmp eax,r8d
jbe WFF_XPZero
push rax
sub rsp,10
movups [rsp],xmm1
cvtsi2sd xmm1,r9
ucomisd xmm0,xmm1
movups xmm1,[rsp]
lea rsp,[rsp+10]
pop rax
jae WFF_XPSetCap
cvttsd2si r9,xmm0
test r9,r9
js WFF_XPZero
add r9,r8
mov esi,r9d
jmp WFF_XPClamp
WFF_XPScaled:
// Invalid (NaN) factor falls back to the unscaled award, without overflow.
mov r9d,esi
add r9,r8
mov esi,r9d
cmp r9,rax
jbe WFF_XPClamp
WFF_XPSetCap:
mov esi,eax
jmp WFF_XPClamp
WFF_XPZero:
mov esi,r8d
WFF_XPClamp:
movups xmm0,[rsp]
add rsp,10
pop r9
cmp eax,esi
jmp WFF_XPReturn
WFF_XPOriginal:
add esi,r8d
cmp eax,esi
WFF_XPReturn:
jmp WFF_XPGain+5
align 10
WFF_XPFactor:
dq (double)1.0
WFF_XPMaxLevel:
db 00

WFF_XPGain:
jmp WFF_XPCode

[DISABLE]
WFF_XPGain:
db 41 03 F0 3B C6
unregistersymbol(WFF_XPFactor)
unregistersymbol(WFF_XPMaxLevel)
unregistersymbol(WFF_XPGain)
dealloc(WFF_XPCode)
'''


def text(parent, tag, value):
    E.SubElement(parent, tag).text = str(value)


def entry(parent, ident, description, script=None, kind=None, address=None, offset=None):
    e = E.SubElement(parent, "CheatEntry")
    text(e, "ID", ident)
    text(e, "Description", f'"{description}"')
    if script:
        text(e, "VariableType", "Auto Assembler Script")
        text(e, "AssemblerScript", script)
    else:
        text(e, "VariableType", kind)
        text(e, "Address", address)
        if offset is not None:
            o=E.SubElement(e,"Offsets")
            text(o,"Offset",offset)
    return e


def main():
    root = E.Element("CheatTable", CheatEngineTableVersion="45")
    entries = E.SubElement(root, "CheatEntries")
    info_guard=(ROOT/'work'/'woff_info_readonly.lua').read_text(encoding='utf-8')
    master_script=BOARD.replace('{$asm}',info_guard+'\n{$asm}',1)
    master=entry(entries,1,"World of Final Fantasy - Original v19 [Enable First]",master_script)
    E.SubElement(master,"Options",moDeactivateChildrenAsWell="1")
    children=E.SubElement(master,"CheatEntries")
    entry(children,10,"Infinite Gil - Hold 9,999,999 [Balance stays after disable]",GIL)
    entry(children,11,"Current Gil (editable)",kind="4 Bytes",address="WOFF.exe+3439EC0",offset="37368")
    for ident,name,offset in ((20,"Ignore SP Cost Requirement",0),
                              (21,"Infinite SP - No Deduction",1)):
        script=f"[ENABLE]\nWFF_CFG+{offset:X}:\ndb 01\n[DISABLE]\nWFF_CFG+{offset:X}:\ndb 00\n"
        entry(children,ident,name,script)
    xp=entry(children,30,"XP Options - Enable [XP/levels update after battle, back on field]",XP)
    E.SubElement(xp,"Options",moDeactivateChildrenAsWell="1")
    xpchildren=E.SubElement(xp,"CheatEntries")
    factor=entry(xpchildren,31,"XP Multiplier (0 = none; 1 = normal; 50000 supported)",kind="Double",address="WFF_XPFactor")
    drop=E.SubElement(factor,"DropDownList",ReadOnly="0",DescriptionOnly="1",DisplayValueAsItem="1")
    drop.text="0:No XP\n1:Normal\n2:2x\n5:5x\n10:10x\n20:20x\n100:100x\n1000:1000x\n50000:50000x"
    entry(xpchildren,32,"Max Level from Next Positive XP Award [Overrides multiplier]",
          "[ENABLE]\nWFF_XPMaxLevel:\ndb 01\n[DISABLE]\nWFF_XPMaxLevel:\ndb 00\n")
    guard=BOARD.split('{$asm}',1)[0].split('[ENABLE]',1)[1]+'{$asm}\n'
    hp=entry(children,40,"Battle HP Options - Enable",HP.replace('[ENABLE]','[ENABLE]'+guard,1))
    E.SubElement(hp,"Options",moDeactivateChildrenAsWell="1")
    hpchildren=E.SubElement(hp,"CheatEntries")
    entry(hpchildren,41,"God Mode - Party HP Damage Blocked [Not status immunity]",
          "[ENABLE]\nWFF_GodMode:\ndb 01\n[DISABLE]\nWFF_GodMode:\ndb 00\n")
    entry(hpchildren,42,"Always Max Health/AP - Living Party, Battle",MAX_VITALS)
    entry(hpchildren,43,"One-Hit Kill - Enemies [Overrides damage multiplier]",
          "[ENABLE]\nWFF_OneHit:\ndb 01\n[DISABLE]\nWFF_OneHit:\ndb 00\n")
    for ident,desc,symbol in ((44,"Player Damage Multiplier (to enemies; 0 = none, 1 = normal)","WFF_PlayerDamage"),
                              (45,"Enemy Damage Multiplier (to party; 0 = none, 1 = normal)","WFF_EnemyDamage")):
        factor=entry(hpchildren,ident,desc,kind="Double",address=symbol)
        drop=E.SubElement(factor,"DropDownList",ReadOnly="0",DescriptionOnly="1",DisplayValueAsItem="1")
        drop.text="0:No damage\n0.25:Quarter damage\n0.5:Half damage\n1:Normal\n2:2x\n5:5x\n10:10x\n100:100x"
    entry(children,50,"Infinite Battle AP - Party Only [Refreshes on AP change]",
          ap_script().replace('[ENABLE]','[ENABLE]'+guard,1))
    entry(children,51,"AP Cost of Abilities Always 0 [Unlocked abilities only]",
          ZERO_AP.replace('[ENABLE]','[ENABLE]'+guard,1))
    items=entry(children,60,"Item Usage Options - Enable [Battle + Field]",
                item_script().replace('[ENABLE]','[ENABLE]'+guard,1))
    E.SubElement(items,"Options",moDeactivateChildrenAsWell="1")
    itemchildren=E.SubElement(items,"CheatEntries")
    for ident,desc,offset in ((61,"Infinite Item Usage [Must own item]",0),
                               (62,"Never Below 1 Item When Used",1)):
        entry(itemchildren,ident,desc,f"[ENABLE]\nWFF_ItemCFG+{offset:X}:\ndb 01\n[DISABLE]\nWFF_ItemCFG+{offset:X}:\ndb 00\n")
    entry(children,70,"Easy Imprism - Conditions + Chance + No Prisms + Library Mirage Permission [Story caution]",
          easy_capture_script().replace('[ENABLE]','[ENABLE]'+guard,1))
    replacement=entry(children,80,"Next Capture Replacement - Enable [Experimental; ONE capture per battle]",
                      replacement_script().replace('[ENABLE]','[ENABLE]'+guard,1))
    E.SubElement(replacement,"Options",moDeactivateChildrenAsWell="1")
    replacement_children=E.SubElement(replacement,"CheatEntries")
    selection=entry(replacement_children,81,"1. Select replacement Mirage [Unusual entries marked; ownership unverified]",
                    kind="4 Bytes",address="WFF_NextCaptureID")
    E.SubElement(selection,"DropDownList",ReadOnly="1",DescriptionOnly="1",DisplayValueAsItem="1").text=mirage_dropdown()
    entry(replacement_children,82,"2. Arm ONE [Replacement appears in Mirage list AFTER battle; off/on to re-arm]",ARM)
    status=entry(replacement_children,83,"INFO ONLY - Arm status [Read-only]",kind="4 Bytes",address="WFF_NextCaptureArmed")
    text(status,'Color','808080')
    E.SubElement(status,"DropDownList",ReadOnly="1",DescriptionOnly="1",DisplayValueAsItem="1").text="0:Idle / consumed\n1:Armed for one capture\n2:Capture queued — finish battle\n3:Processing"
    for ident,desc,symbol in ((84,"INFO ONLY - Last original species [Read-only]","WFF_LastCaptureSourceID"),
                             (85,"INFO ONLY - Last replacement species [Read-only; verify in Mirage list]","WFF_LastCaptureSelectedID")):
        info=entry(replacement_children,ident,desc,kind="4 Bytes",address=symbol)
        text(info,'Color','808080')
        E.SubElement(info,"DropDownList",ReadOnly="1",DescriptionOnly="1",DisplayValueAsItem="1").text=mirage_dropdown().replace('0:Select a Mirage first — no replacement','0:No replacement recorded',1)
    entry(children,90,"Save Anywhere - Field Menu [Reopen menu after toggling; separate save slot recommended]",
          SAVE.replace('[ENABLE]','[ENABLE]'+guard,1))
    entry(children,100,"Guaranteed Enemy Loot Rolls [TEST; positive-chance drops only; defeat enemies]",
          LOOT.replace('[ENABLE]','[ENABLE]'+guard,1))
    buffs=entry(children,110,"Party Battle Status Options - Enable [TEST]",
                STATUS.replace('[ENABLE]','[ENABLE]'+guard,1))
    E.SubElement(buffs,"Options",moDeactivateChildrenAsWell="1")
    buffchildren=E.SubElement(buffs,"CheatEntries")
    for ident,desc,offset in ((111,"Always Haste - Living Party [TEST]",0),
                              (112,"Always Regen - Living Party [TEST]",1),
                              (113,"Always Protect / Shell - Living Party [TEST]",2),
                              (114,"Positive Buffs Never Expire - Party [TEST; excludes Reflect/Berserk]",3),
                              (115,"Block Negative Statuses - Party [TEST; does not block KO or cure existing effects]",4)):
        entry(buffchildren,ident,desc,f"[ENABLE]\nWFF_StatusCFG+{offset:X}:\ndb 01\n[DISABLE]\nWFF_StatusCFG+{offset:X}:\ndb 00\n")
    entry(children,116,"Always Critical - Party [Critical-capable attacks only]",CRITICAL.replace('[ENABLE]','[ENABLE]'+guard,1))
    entry(children,117,"Party Stacks Never Topple [TEST; balance damage; manual unstack still allowed]",STACK.replace('[ENABLE]','[ENABLE]'+guard,1))
    entry(children,118,"Never Miss - Party [TEST; enable in battle; normal accuracy checks only]",ACCURACY.replace('[ENABLE]','[ENABLE]'+guard,1))
    entry(children,119,"Topple One Enemy Stack - F8 [Press F8, then Defend before enemy turn; no HP damage]",topple_script())
    text(root,"UserdefinedSymbols","")
    text(root,"Comments", "Original implementation. DrummerIX reference CT was read for context only; "
         "addresses and machine instructions were independently checked in the running game. "
         "No third-party scripts are embedded. Enable parent first; this also installs UI-only "
         "read-only guards on grey INFO ONLY rows. Those rows cannot be frozen or edited through "
         "ordinary table controls; selectors and multiplier values remain editable. "
         "Confirmed gameplay features have no Test tag. Experimental limitations remain labelled. "
         "Disable children before parent, and disable everything before closing Cheat Engine. "
         "Gil changes remain after disabling. SP options share hooks and can be combined. "
         "XP and level changes become visible after battle, when back on the field. "
         "User confirmed foundation scripts work in gameplay on 2026-10-10. "
         "User also confirmed v3 God Mode and Infinite Battle AP work. "
         "User confirmed v4 damage and max-vitals options work. One-Hit Kill overrides the player multiplier; "
         "God Mode and Always Max override the enemy multiplier. Multipliers operate by target side, "
         "not attacker identity. Healing and zero-damage hits are not multiplied. "
         "Enable Always Max in battle; if party actors are rebuilt, retoggle it to rediscover them. "
         "Always Max does not revive KO actors; refilled values remain after disabling. "
         "v5 adds zero ability AP costs and two shared-hook item consumption modes. "
         "Infinite Usage overrides Never Below 1. Item routines may also serve non-use inventory removal; "
         "disable item options for selling, crafting, or quest hand-ins until tested. "
         "User confirmed v5 options work in gameplay. v6 adds Easy Imprism readiness and chance hooks "
         "for known enemy Mirage actors with a native capture capability. Native Prism, living-target, "
         "and other eligibility checks remain. No actor capture-state fields are edited. "
         "User confirmed v6 captures Mu; Chocochicks were blocked by missing required Prism, not their "
         "species conditions. v7 merges capture-only Prism requirement and consumption bypass into "
         "Easy Imprism to capture eligible Mirages without meeting their "
         "normal readiness condition or owning their Prism. Native living-target, capture-state, and "
         "battle restrictions remain; this does not promise boss/uncapturable support. "
         "User confirmed v7 captures a Chocochick with no Prism. "
         "v8 replacement failed: visual clone changed but ownership did not. v9 queues one successful "
         "capture and changes only its native owned-grant argument. "
         "Enable its parent, select a species, then arm. "
         "It starts disarmed. The arm flag is consumed once; toggle Arm off/on to re-arm. "
         "Status 2 means queued; finish the battle without re-arming or disabling replacement. "
         "The capture animation remains the original species. "
         "The user verified Mu-to-Chocochick and Mu-to-Goblin ownership replacement on 2026-10-10; live primary "
         "and board/form IDs agree. All battle/capture visuals may still show the original Mirage "
         "until fully out of battle: check the Mirage list afterward. Only one capture per battle "
         "is validated; other species, multiple captures and reloading saved replacements are untested. "
         "A 0 status means idle/consumed, not proof the selected species is safe or that a free "
         "ownership slot was available. "
         "Native construction receives the chosen ID; enemy IDs remain unchanged. "
         "264 candidates were independently decoded from installed definitions; 248 are library-listed. "
         "Unused/test/outside-library entries are labelled, not certified ownable. Library membership "
         "does not guarantee safety. Back up saves and initially test a normal species. "
         "Verify appearance, board, abilities and stats before saving a replacement result. "
         "Do not freeze informational fields. Champion-cost is not implemented. "
         "v11 bypasses only the field-menu Save entry's required permission flag. Close/reopen the "
         "menu after toggling. Does not save automatically or enable battle/cutscene menus. "
         "User confirmed field saving and reloading on 2026-10-10. Other maps/story states remain "
         "untested; a separate save slot is recommended. v12 fixes disable-time address resolution. "
         "No save-writing routines or persistent event flags are modified. "
         "v15 added party status, critical and stack-balance options. User confirmed critical attacks "
         "in gameplay; the other new battle options retain TEST labels. "
         "v16 adds a reversible loaded-script normal accuracy result override for player-side attackers "
         "only. Enable Never Miss while in battle. Enemy accuracy, deliberate-miss, resurrection and "
         "capture routines are not altered. It does not bypass immunity or scripted battle rules. "
         "If the battle script VM is rebuilt, retoggle in battle. Gameplay verification is pending. "
         "v18 repairs stacked-member status propagation, includes verified Lann/Reynn classes in "
         "party status filters, and maintains native Protect/Shell counters when duration protection "
         "is selected. Buff application requires battle time to advance (choose Defend). "
         "Easy Imprism now bypasses encounter capture permission only for library-listed enemy "
         "Mirage species, including Behemoth, without changing their actor permission fields. "
         "Both native eligibility and the UI permission binding are covered; living-target, "
         "capture-state and other battle checks still run. This does not promise all bosses or "
         "scripted encounters are safe: capturing a story opponent may affect progression. "
         "Use a separate save and verify the owned Mirage after battle.")
    root.find('Comments').text += (
         " User confirmed Behemoth capture succeeds with v18 on 2026-10-10. "
         "Live status masks were verified on both party stacks and all four members after Defend, "
         "with enemy status unchanged. Buff effects across later battles remain under testing. "
         "v19 adds an F8 one-shot enemy topple experiment. Enable the entry, then press F8 in battle. "
         "It dispatches the native collapse binding from the game's actor-update thread, not a CE "
         "worker thread. Only living enemy UnitTower actors with two or three members are eligible; "
         "no HP, party balance, capture or ownership fields are changed. One stack per press. "
         "Unconsumed requests expire after three seconds. If the command menu pauses battle time, "
         "press F8 immediately before choosing Defend, just before the enemy's turn. "
         "User confirmed this topples the Mini Golem/Copper Gnome stack on 2026-10-10. "
         "It is queued, not an immediate command-menu animation. Other encounters remain untested.")
    E.indent(root, space="  ")
    target=ROOT/"outputs"/"World of Final Fantasy - Original v19.CT"
    E.ElementTree(root).write(target,encoding="utf-8",xml_declaration=True)
    (ROOT/'work'/'woff-save.aa').write_text(SAVE.replace('[ENABLE]','[ENABLE]'+guard,1),encoding='utf-8')
    (ROOT/'work'/'woff-loot.aa').write_text(LOOT.replace('[ENABLE]','[ENABLE]'+guard,1),encoding='utf-8')
    (ROOT/'work'/'woff-status.aa').write_text(STATUS.replace('[ENABLE]','[ENABLE]'+guard,1),encoding='utf-8')
    (ROOT/'work'/'woff-capture-v18.aa').write_text(easy_capture_script().replace('[ENABLE]','[ENABLE]'+guard,1),encoding='utf-8')
    (ROOT/'work'/'woff-critical.aa').write_text(CRITICAL.replace('[ENABLE]','[ENABLE]'+guard,1),encoding='utf-8')
    (ROOT/'work'/'woff-stack.aa').write_text(STACK.replace('[ENABLE]','[ENABLE]'+guard,1),encoding='utf-8')
    (ROOT/'work'/'woff-accuracy.aa').write_text(ACCURACY.replace('[ENABLE]','[ENABLE]'+guard,1),encoding='utf-8')
    (ROOT/'work'/'woff-topple.aa').write_text(topple_script(),encoding='utf-8')
    print(target)


if __name__ == "__main__":
    main()
