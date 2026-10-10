"""Original cost and inventory consumption hooks, authored from live disassembly."""

ZERO_AP = r'''[ENABLE]
aobscanmodule(WFF_AbilityCost,WOFF.exe,48 83 EC 38 80 BA EC 01 00 00 00 48 8B C1 0F 29 74 24 20)
assert(WFF_AbilityCost,48 83 EC 38 80 BA EC 01 00 00 00)
alloc(WFF_AbilityCostCode,256,WFF_AbilityCost)
label(WFF_CostCheckSide)
label(WFF_CostOriginal)
registersymbol(WFF_AbilityCost)
WFF_AbilityCostCode:
pushfq
// RCX points at actor statistics (+29B0), not the whole actor.
mov rax,WOFF.exe+2F4B168
cmp [rcx-29B0],rax
je WFF_CostCheckSide
mov rax,WOFF.exe+2F39FC0
cmp [rcx-29B0],rax
jne WFF_CostOriginal
WFF_CostCheckSide:
cmp dword ptr [rcx+484],0
jne WFF_CostOriginal
popfq
xorps xmm0,xmm0
ret
WFF_CostOriginal:
popfq
sub rsp,38
cmp byte ptr [rdx+1EC],0
jmp WFF_AbilityCost+B
WFF_AbilityCost:
jmp WFF_AbilityCostCode
nop 6
// Party command menu affordability and both cost-icon views.
aobscanmodule(WFF_CostMenu,WOFF.exe,F3 0F 10 70 1C 4D 85 DB 74 3C 49 8B 43 20)
aobscanmodule(WFF_CostIcons,WOFF.exe,F3 0F 10 40 1C F3 0F 59 05 4D 52 92 02)
aobscanmodule(WFF_CostIcons2,WOFF.exe,F3 0F 10 40 1C 49 8B 43 20 F3 0F 59 C6)
assert(WFF_CostMenu,F3 0F 10 70 1C)
assert(WFF_CostIcons,F3 0F 10 40 1C)
assert(WFF_CostIcons2,F3 0F 10 40 1C)
registersymbol(WFF_CostMenu)
registersymbol(WFF_CostIcons)
registersymbol(WFF_CostIcons2)
WFF_CostMenu:
xorps xmm6,xmm6
nop 2
WFF_CostIcons:
xorps xmm0,xmm0
nop 2
WFF_CostIcons2:
xorps xmm0,xmm0
nop 2
[DISABLE]
WFF_AbilityCost:
db 48 83 EC 38 80 BA EC 01 00 00 00
WFF_CostMenu:
db F3 0F 10 70 1C
WFF_CostIcons:
db F3 0F 10 40 1C
WFF_CostIcons2:
db F3 0F 10 40 1C
unregistersymbol(WFF_AbilityCost)
unregistersymbol(WFF_CostMenu)
unregistersymbol(WFF_CostIcons)
unregistersymbol(WFF_CostIcons2)
dealloc(WFF_AbilityCostCode)
'''


def item_script():
    # All hooks are AFTER the game's ownership/quantity check. Never creates an
    # unowned item or changes inventory IDs, completion flags or success returns.
    paths = [
        ('Single','rax','ecx','FF C9 41 BA 01 00 00 00 89 48 04 48 8B 5C 24 08',
         'FF C9 41 BA 01 00 00 00',8,'dec ecx','mov r10d,1'),
        ('Misc','rax','ecx','41 2B CA 89 48 04 85 C9 7F 0A C7 00 FF FF FF FF',
         '41 2B CA 89 48 04',6,'sub ecx,r10d','mov [rax+4],ecx'),
        ('Battle','rdx','eax','41 2B C2 89 42 04 85 C0 7F 0A C7 02 FF FF FF FF',
         '41 2B C2 89 42 04',6,'sub eax,r10d','mov [rdx+4],eax'),
    ]
    lines=['[ENABLE]']
    for name,ptr,reg,signature,original,length,arithmetic,tail in paths:
        s='WFF_Item'+name
        lines += [f'aobscanmodule({s},WOFF.exe,{signature})',f'assert({s},{original})',
                  f'alloc({s}Code,256,{s})',f'label({s}Keep)',f'label({s}Finish)',
                  f'registersymbol({s})']
    lines += ['label(WFF_ItemCFG)','registersymbol(WFF_ItemCFG)']
    for name,ptr,reg,signature,original,length,arithmetic,tail in paths:
        s='WFF_Item'+name
        lines += [f'{s}Code:',arithmetic,'pushfq']
        if name!='Single':
            lines += ['test r10d,r10d',f'jle {s}Finish']
        lines += ['cmp byte ptr [WFF_ItemCFG],0',f'je {s}Keep',
                  f'mov {reg},[{ptr}+4]',f'jmp {s}Finish',f'{s}Keep:',
                  'cmp byte ptr [WFF_ItemCFG+1],0',f'je {s}Finish',
                  f'test {reg},{reg}',f'jg {s}Finish',f'mov {reg},1',
                  f'{s}Finish:','popfq',tail,f'jmp {s}+{length:X}',
                  f'{s}:',f'jmp {s}Code',f'nop {length-5}']
    lines += ['WFF_ItemSingleCode+E0:','WFF_ItemCFG:','db 00 00','[DISABLE]']
    for name,ptr,reg,signature,original,length,arithmetic,tail in paths:
        s='WFF_Item'+name
        lines += [f'{s}:',f'db {original}',f'unregistersymbol({s})',f'dealloc({s}Code)']
    lines += ['unregistersymbol(WFF_ItemCFG)']
    return '\n'.join(lines)+'\n'
