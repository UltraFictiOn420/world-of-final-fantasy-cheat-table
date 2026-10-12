"""Original bounded, single-battle multi-capture replacement prototype.

Enable and arm before the first capture; keep enabled through every result screen.
Re-enable the parent for another battle. Native allocation/grant logic is unchanged.
"""
from pathlib import Path
from woff_replacement_options import candidates


def replacement_script():
    ids = sorted(r['id'] for r in candidates())
    allow = '\n'.join('dd ' + ' '.join(f'{v:X}' for v in ids[i:i+12])
                      for i in range(0, len(ids), 12))
    return r'''[ENABLE]
aobscanmodule(WFF_CloneArgs,WOFF.exe,44 8B CB 89 7C 24 20 44 8B C0 48 8D 54 24 58 49 8B CE E8 69 F4 FF FF)
aobscanmodule(WFF_ClonePost,WOFF.exe,48 8B BE 80 1B 00 00 48 85 FF 74 5D 48 8B 4F 08 32 DB)
aobscanmodule(WFF_NamingPrepare,WOFF.exe,48 8B 87 00 08 00 00 48 8D 14 88 48 8B 0D)
define(WFF_CloneArgsHook,WFF_CloneArgs+7)
assert(WFF_CloneArgsHook,44 8B C0 48 8D 54 24 58)
assert(WFF_ClonePost,48 8B BE 80 1B 00 00)
assert(WFF_NamingPrepare,48 8B 87 00 08 00 00)
alloc(WFF_ReplacementCode,4000,WFF_CloneArgsHook)
label(WFF_QueueNative)
label(WFF_QueueLoop)
label(WFF_QueueFound)
label(WFF_DedupeLoop)
label(WFF_DedupeNext)
label(WFF_Reserve)
label(WFF_ClonePostCode)
label(WFF_ClonePostNative)
label(WFF_NamingPrepareCode)
label(WFF_NamingPrepareNative)
label(WFF_ValidateLoop)
label(WFF_ApplyLoop)
label(WFF_ApplySkip)
label(WFF_NamingReject)
label(WFF_NextCaptureID)
label(WFF_NextCaptureArmed)
label(WFF_LastCaptureSourceID)
label(WFF_LastCaptureSelectedID)
label(WFF_CaptureCount)
label(WFF_CaptureRows)
label(WFF_CaptureAllowedIDs)
label(WFF_NamingPrepared)
label(WFF_VisualChanges)
label(WFF_NamingChanges)
registersymbol(WFF_CloneArgsHook)
registersymbol(WFF_ClonePost)
registersymbol(WFF_NamingPrepare)
registersymbol(WFF_NextCaptureID)
registersymbol(WFF_NextCaptureArmed)
registersymbol(WFF_LastCaptureSourceID)
registersymbol(WFF_LastCaptureSelectedID)
registersymbol(WFF_CaptureCount)
registersymbol(WFF_CaptureRows)
registersymbol(WFF_NamingPrepared)
registersymbol(WFF_VisualChanges)
registersymbol(WFF_NamingChanges)

WFF_ReplacementCode:
mov r8d,eax
lea rdx,[rsp+58]
pushfq
push rax
push rcx
push r10
push r11
// One enabled session handles exactly one battle. Record every capture, even
// unselected ones, so list alignment cannot silently shift over an original.
cmp dword ptr [WFF_NamingPrepared],0
jne WFF_QueueNative
mov r10,WOFF.exe+5A0D0F
cmp [rsp+70],r10
jne WFF_QueueNative
mov r10,WOFF.exe+2F39FC0
cmp [rsi],r10
jne WFF_QueueNative
cmp dword ptr [rsi+2E34],1
jne WFF_QueueNative
// Easy Imprism can permit a successful capture while native permission is zero.
// Qualify the actual capture clone path below, not the old permission flag.
mov r10,WOFF.exe+2F33B50
cmp [r14],r10
jne WFF_QueueNative
cmp dword ptr [rsp+88],1
jne WFF_QueueNative
cmp dword ptr [rsp+90],1
jne WFF_QueueNative
mov ecx,[WFF_CaptureCount]
cmp ecx,#32
jae WFF_QueueNative
lea r10,[WFF_CaptureRows]
xor eax,eax
WFF_DedupeLoop:
cmp eax,ecx
jae WFF_Reserve
// Animation clone storage may be recycled after an earlier capture finishes.
// Only the SAME source actor AND same clone constitutes a duplicate observation.
cmp [r10+8],rsi
jne WFF_DedupeNext
cmp [r10+10],r14
je WFF_QueueNative
WFF_DedupeNext:
add r10,20
inc eax
jmp WFF_DedupeLoop
WFF_Reserve:
mov [r10],r8d
mov dword ptr [r10+4],0
mov [r10+8],rsi
mov [r10+10],r14
inc dword ptr [WFF_CaptureCount]
cmp dword ptr [WFF_NextCaptureArmed],1
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
// Selection is snapshotted for THIS capture; later dropdown changes cannot
// overwrite an earlier pending result. Arming remains on for further captures.
mov eax,[WFF_CaptureCount]
dec eax
shl eax,5
lea r10,[WFF_CaptureRows]
add r10,rax
mov [r10+4],r11d
mov [WFF_LastCaptureSourceID],r8d
mov r8d,r11d
mov dword ptr [rsp+48],0
mov dword ptr [rsp+88],80000000
inc dword ptr [WFF_VisualChanges]
WFF_QueueNative:
pop r11
pop r10
pop rcx
pop rax
popfq
jmp WFF_CloneArgsHook+8

WFF_ClonePostCode:
pushfq
cmp dword ptr [rsp+68],80000000
jne WFF_ClonePostNative
popfq
mov dword ptr [rsp+60],0
xor edx,edx
jmp WFF_ClonePost+6F
WFF_ClonePostNative:
popfq
mov rdi,[rsi+1B80]
jmp WFF_ClonePost+7

WFF_NamingPrepareCode:
pushfq
push rax
push rcx
push rdx
push r10
push r11
cmp dword ptr [WFF_NamingPrepared],0
jne WFF_NamingPrepareNative
cmp dword ptr [rdi+824],0
jne WFF_NamingPrepareNative
test rcx,rcx
jnz WFF_NamingPrepareNative
mov ecx,[WFF_CaptureCount]
test ecx,ecx
jz WFF_NamingPrepareNative
cmp ecx,#32
ja WFF_NamingReject
mov r10,[rdi+800]
test r10,r10
jz WFF_NamingReject
mov rax,[rdi+808]
sub rax,r10
mov edx,ecx
shl edx,2
cmp rax,rdx
jne WFF_NamingReject
// Validate ALL original entries before touching ANY. The native list shrinks
// at its front, and this preparation runs only once for the entire batch.
lea r11,[WFF_CaptureRows]
WFF_ValidateLoop:
mov eax,[r11]
cmp [r10],eax
jne WFF_NamingReject
add r10,4
add r11,20
dec ecx
jne WFF_ValidateLoop
mov ecx,[WFF_CaptureCount]
mov r10,[rdi+800]
lea r11,[WFF_CaptureRows]
WFF_ApplyLoop:
mov eax,[r11+4]
test eax,eax
jz WFF_ApplySkip
mov [r10],eax
mov [WFF_LastCaptureSelectedID],eax
inc dword ptr [WFF_NamingChanges]
WFF_ApplySkip:
add r10,4
add r11,20
dec ecx
jne WFF_ApplyLoop
mov dword ptr [WFF_NamingPrepared],1
mov dword ptr [WFF_NextCaptureArmed],0
jmp WFF_NamingPrepareNative
WFF_NamingReject:
// Fail closed on missing/reordered observations: no result IDs are changed.
mov dword ptr [WFF_NamingPrepared],2
mov dword ptr [WFF_NextCaptureArmed],0
WFF_NamingPrepareNative:
pop r11
pop r10
pop rdx
pop rcx
pop rax
popfq
mov rax,[rdi+800]
jmp WFF_NamingPrepare+7

align 10
WFF_NextCaptureID:
dd 0
WFF_NextCaptureArmed:
dd 0
WFF_LastCaptureSourceID:
dd 0
WFF_LastCaptureSelectedID:
dd 0
WFF_CaptureCount:
dd 0
WFF_NamingPrepared:
dd 0
WFF_VisualChanges:
dd 0
WFF_NamingChanges:
dd 0
align 10
WFF_CaptureRows:
// 32 records, each source ID, selected ID, source actor, clone actor, padding.
@ROWS@
WFF_CaptureAllowedIDs:
@ALLOWLIST@

WFF_CloneArgsHook:
jmp WFF_ReplacementCode
nop 3
WFF_ClonePost:
jmp WFF_ClonePostCode
nop 2
WFF_NamingPrepare:
jmp WFF_NamingPrepareCode
nop 2
[DISABLE]
WFF_NamingPrepare:
db 48 8B 87 00 08 00 00
WFF_ClonePost:
db 48 8B BE 80 1B 00 00
WFF_CloneArgsHook:
db 44 8B C0 48 8D 54 24 58
unregistersymbol(WFF_CloneArgsHook)
unregistersymbol(WFF_ClonePost)
unregistersymbol(WFF_NamingPrepare)
unregistersymbol(WFF_NextCaptureID)
unregistersymbol(WFF_NextCaptureArmed)
unregistersymbol(WFF_LastCaptureSourceID)
unregistersymbol(WFF_LastCaptureSelectedID)
unregistersymbol(WFF_CaptureCount)
unregistersymbol(WFF_CaptureRows)
unregistersymbol(WFF_NamingPrepared)
unregistersymbol(WFF_VisualChanges)
unregistersymbol(WFF_NamingChanges)
dealloc(WFF_ReplacementCode)
'''.replace('@COUNT@', f'{len(ids):X}').replace('@ALLOWLIST@', allow).replace(
        '@ROWS@', '\n'.join('dq 0 0 0 0' for _ in range(32)))


if __name__ == '__main__':
    Path(__file__).with_name('woff-multicapture-replacement.aa').write_text(
        replacement_script(), encoding='utf-8')
