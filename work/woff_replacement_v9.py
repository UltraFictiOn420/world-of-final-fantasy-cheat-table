"""Two-stage replacement: observe successful capture, replace its owned grant.

The previous v8 code initialized a visual clone, not the owned record. This version
never changes that clone, the source actor, or any existing owned Mirage.
"""
from woff_replacement_options import candidates, dropdown, ARM


def replacement_script():
    ids = sorted(r['id'] for r in candidates())
    allowlist = '\n'.join('dd ' + ' '.join(f'{x:X}' for x in ids[i:i+12])
                          for i in range(0, len(ids), 12))
    script = r'''[ENABLE]
aobscanmodule(WFF_CloneArgs,WOFF.exe,44 8B CB 89 7C 24 20 44 8B C0 48 8D 54 24 58 49 8B CE E8 69 F4 FF FF)
aobscanmodule(WFF_OwnedGrant,WOFF.exe,48 89 5C 24 08 48 89 6C 24 10 48 89 74 24 18 57 48 83 EC 40 8B DA 48 C7 44 24 30 00 00 00 00)
define(WFF_CloneArgsHook,WFF_CloneArgs+7)
assert(WFF_CloneArgsHook,44 8B C0 48 8D 54 24 58)
assert(WFF_OwnedGrant,48 89 5C 24 08)
alloc(WFF_ReplacementCode,2048,WFF_CloneArgsHook)
label(WFF_QueueNative)
label(WFF_QueueLoop)
label(WFF_QueueFound)
label(WFF_GrantCode)
label(WFF_GrantNative)
label(WFF_NextCaptureID)
label(WFF_NextCaptureArmed)
label(WFF_LastCaptureSourceID)
label(WFF_LastCaptureSelectedID)
label(WFF_PendingCaptureID)
label(WFF_CaptureAllowedIDs)
registersymbol(WFF_CloneArgsHook)
registersymbol(WFF_OwnedGrant)
registersymbol(WFF_NextCaptureID)
registersymbol(WFF_NextCaptureArmed)
registersymbol(WFF_LastCaptureSourceID)
registersymbol(WFF_LastCaptureSelectedID)

WFF_ReplacementCode:
// Visual clone runs unchanged. Queue a choice only on the observed capture path.
mov r8d,eax
lea rdx,[rsp+58]
pushfq
push rax
push rcx
push r10
push r11
cmp dword ptr [WFF_NextCaptureArmed],1
jne WFF_QueueNative
mov r10,WOFF.exe+5A0D0F
cmp [rsp+70],r10
jne WFF_QueueNative
mov r10,WOFF.exe+2F39FC0
cmp [rsi],r10
jne WFF_QueueNative
cmp dword ptr [rsi+2E34],1
jne WFF_QueueNative
cmp dword ptr [rsi+2B40],0
jle WFF_QueueNative
mov r10,WOFF.exe+2F33B50
cmp [r14],r10
jne WFF_QueueNative
cmp dword ptr [rsp+88],1
jne WFF_QueueNative
cmp dword ptr [rsp+90],1
jne WFF_QueueNative
mov r11d,[WFF_NextCaptureID]
lea r10,[WFF_CaptureAllowedIDs]
mov ecx,@COUNT@
WFF_QueueLoop:
cmp r11d,[r10]
je WFF_QueueFound
add r10,4
dec ecx
jne WFF_QueueLoop
jmp WFF_QueueNative
WFF_QueueFound:
// 3 is a brief internal reservation. Publish 2 only after queue fields are ready.
mov eax,1
mov ecx,3
lock cmpxchg [WFF_NextCaptureArmed],ecx
jne WFF_QueueNative
mov [WFF_PendingCaptureID],r11d
mov [WFF_LastCaptureSourceID],r8d
mov dword ptr [WFF_LastCaptureSelectedID],0
mov dword ptr [WFF_NextCaptureArmed],2
WFF_QueueNative:
pop r11
pop r10
pop rcx
pop rax
popfq
jmp WFF_CloneArgsHook+8

WFF_GrantCode:
pushfq
push rax
push rcx
push r10
push r11
cmp dword ptr [WFF_NextCaptureArmed],2
jne WFF_GrantNative
// Confirmed by the TraceMu capture: other awards/party reconstruction bypass.
mov r10,WOFF.exe+734FC7
cmp [rsp+28],r10
jne WFF_GrantNative
mov r10,[WOFF.exe+3439EC0]
lea r10,[r10+D0]
cmp rcx,r10
jne WFF_GrantNative
cmp edx,[WFF_LastCaptureSourceID]
jne WFF_GrantNative
mov r11d,[WFF_PendingCaptureID]
test r11d,r11d
jz WFF_GrantNative
mov eax,2
mov ecx,3
lock cmpxchg [WFF_NextCaptureArmed],ecx
jne WFF_GrantNative
// Native free-slot allocation and species/board/stats construction stay intact.
mov edx,r11d
xor r8d,r8d
mov [WFF_LastCaptureSelectedID],r11d
mov dword ptr [WFF_PendingCaptureID],0
mov dword ptr [WFF_NextCaptureArmed],0
WFF_GrantNative:
pop r11
pop r10
pop rcx
pop rax
popfq
mov [rsp+8],rbx
jmp WFF_OwnedGrant+5

align 10
WFF_NextCaptureID:
dd 0
WFF_NextCaptureArmed:
dd 0
WFF_LastCaptureSourceID:
dd 0
WFF_LastCaptureSelectedID:
dd 0
WFF_PendingCaptureID:
dd 0
WFF_CaptureAllowedIDs:
@ALLOWLIST@

WFF_CloneArgsHook:
jmp WFF_ReplacementCode
nop 3
WFF_OwnedGrant:
jmp WFF_GrantCode
[DISABLE]
WFF_CloneArgsHook:
db 44 8B C0 48 8D 54 24 58
WFF_OwnedGrant:
db 48 89 5C 24 08
unregistersymbol(WFF_CloneArgsHook)
unregistersymbol(WFF_OwnedGrant)
unregistersymbol(WFF_NextCaptureID)
unregistersymbol(WFF_NextCaptureArmed)
unregistersymbol(WFF_LastCaptureSourceID)
unregistersymbol(WFF_LastCaptureSelectedID)
dealloc(WFF_ReplacementCode)
'''
    return script.replace('@COUNT@', f'{len(ids):X}').replace('@ALLOWLIST@', allowlist)


if __name__ == '__main__':
    from pathlib import Path
    Path(__file__).with_name('woff-replacement-v9.aa').write_text(
        replacement_script(), encoding='utf-8')
