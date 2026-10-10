"""Original native-thread party buff experiments, verified 2.0.0.0 anchors."""

STATUS = r'''[ENABLE]
aobscanmodule(WFF_StatusTick,WOFF.exe,85 87 B0 2A 00 00 0F 84 D7 09 00 00 46 0F 2F 84 AF 7C 33 00 00)
aobscanmodule(WFF_StatusApply,WOFF.exe,44 89 4C 24 20 89 54 24 10 55 53 56 57 41 55 41 56 41 57)
assert(WFF_StatusTick,85 87 B0 2A 00 00)
assert(WFF_StatusApply,44 89 4C 24 20)
alloc(WFF_StatusCode,4096,WFF_StatusTick)
label(WFF_StatusCFG)
label(WFF_StatusOriginal)
label(WFF_StatusSaved)
label(WFF_StatusWanted)
label(WFF_StatusPresent)
label(WFF_StatusFreeze)
label(WFF_StatusApplyCode)
label(WFF_StatusApplyOriginal)
label(WFF_StatusDenied)
label(WFF_StatusCalls)
label(WFF_StatusNeedApply)
label(WFF_StatusMemberLoop)
label(WFF_StatusMembersPresent)
label(WFF_StatusMemberMissing)
registersymbol(WFF_StatusTick)
registersymbol(WFF_StatusApply)
registersymbol(WFF_StatusCFG)
registersymbol(WFF_StatusCalls)
WFF_StatusCode:
pushfq
push rax
cmp dword ptr [rdi+2E34],0
jne WFF_StatusOriginal
mov rax,WOFF.exe+2F39FC0
cmp [rdi],rax
je WFF_StatusSaved
mov rax,WOFF.exe+2F4B168
cmp [rdi],rax
je WFF_StatusSaved
// Independently observed player-character/partner classes, including members.
mov rax,WOFF.exe+2F49E78
cmp [rdi],rax
je WFF_StatusSaved
mov rax,WOFF.exe+2F3DF30
cmp [rdi],rax
jne WFF_StatusOriginal
WFF_StatusSaved:
// This is inside the native battle update, not a CE worker thread.
// r12d/r13 identify the current status, and remain nonvolatile across calls.
cmp dword ptr [rdi+29C8],0
jle WFF_StatusOriginal
cmp r12d,0D
jne @f
cmp byte ptr [WFF_StatusCFG],0
jne WFF_StatusWanted
@@:
cmp r12d,0C
jne @f
cmp byte ptr [WFF_StatusCFG+1],0
jne WFF_StatusWanted
@@:
cmp r12d,9
je @f
cmp r12d,0A
jne WFF_StatusFreeze
@@:
cmp byte ptr [WFF_StatusCFG+2],0
je WFF_StatusFreeze
WFF_StatusWanted:
mov eax,[rdi+2AB0]
bt eax,r12d
jnc WFF_StatusNeedApply
// A stack's own flag alone does not prove its members received the status.
mov rax,WOFF.exe+2F4B168
cmp [rdi],rax
jne WFF_StatusPresent
push r8
push r9
mov r8,[rdi+3690]
mov r9,[rdi+3698]
mov rax,r9
sub rax,r8
cmp rax,18
ja WFF_StatusMembersPresent
WFF_StatusMemberLoop:
cmp r8,r9
jae WFF_StatusMembersPresent
mov rax,[r8]
test rax,rax
jz @f
cmp dword ptr [rax+29C8],0
jle @f
mov eax,[rax+2AB0]
bt eax,r12d
jnc WFF_StatusMemberMissing
@@:
add r8,8
jmp WFF_StatusMemberLoop
WFF_StatusMembersPresent:
pop r9
pop r8
jmp WFF_StatusPresent
WFF_StatusMemberMissing:
pop r9
pop r8
WFF_StatusNeedApply:
// Preserve every volatile register and provide x64 shadow/stack arguments.
push rcx
push rdx
push r8
push r9
push r10
push r11
sub rsp,0A0
movups [rsp+40],xmm0
movups [rsp+50],xmm1
movups [rsp+60],xmm2
movups [rsp+70],xmm3
movups [rsp+80],xmm4
movups [rsp+90],xmm5
mov rcx,rdi
mov edx,r12d
mov r8d,1
xor r9d,r9d
mov dword ptr [rsp+20],1
mov qword ptr [rsp+28],0
// Native seventh argument: zero propagates stack status to its members.
mov dword ptr [rsp+30],0
mov rax,[rdi]
call qword ptr [rax+700]
inc dword ptr [WFF_StatusCalls]
movups xmm0,[rsp+40]
movups xmm1,[rsp+50]
movups xmm2,[rsp+60]
movups xmm3,[rsp+70]
movups xmm4,[rsp+80]
movups xmm5,[rsp+90]
add rsp,0A0
pop r11
pop r10
pop r9
pop r8
pop rdx
pop rcx
WFF_StatusPresent:
WFF_StatusFreeze:
cmp byte ptr [WFF_StatusCFG+3],0
je WFF_StatusOriginal
// Explicit beneficial-status allowlist; no KO, Reflect or Berserk.
mov eax,0AABB600
bt eax,r12d
jnc WFF_StatusOriginal
mov eax,[rdi+2AB0]
bt eax,r12d
jnc WFF_StatusOriginal
// Protect/Shell have native hit counters as well as duration slots.
cmp r12d,9
jne @f
cmp dword ptr [rdi+3414],2
jae @f
mov dword ptr [rdi+3414],2
@@:
cmp r12d,0A
jne @f
cmp dword ptr [rdi+3418],2
jae @f
mov dword ptr [rdi+3418],2
@@:
cmp r12d,0C
je @f
// Keep non-Regen clocks positive, but let native Regen ticks run.
cmp dword ptr [rdi+r13*4+337C],3F800000
jae WFF_StatusOriginal
mov dword ptr [rdi+r13*4+337C],3F800000
jmp WFF_StatusOriginal
@@:
cmp dword ptr [rdi+3420],2
jge WFF_StatusOriginal
mov dword ptr [rdi+3420],2
WFF_StatusOriginal:
pop rax
popfq
test dword ptr [rdi+2AB0],eax
jmp WFF_StatusTick+6

WFF_StatusApplyCode:
pushfq
push rax
cmp byte ptr [WFF_StatusCFG+4],0
je WFF_StatusApplyOriginal
test r8d,r8d
je WFF_StatusApplyOriginal
cmp dword ptr [rcx+2E34],0
jne WFF_StatusApplyOriginal
mov rax,WOFF.exe+2F39FC0
cmp [rcx],rax
je @f
mov rax,WOFF.exe+2F4B168
cmp [rcx],rax
je @f
mov rax,WOFF.exe+2F49E78
cmp [rcx],rax
je @f
mov rax,WOFF.exe+2F3DF30
cmp [rcx],rax
jne WFF_StatusApplyOriginal
@@:
cmp edx,1
jb WFF_StatusApplyOriginal
cmp edx,1C
ja WFF_StatusApplyOriginal
mov eax,155441FE
bt eax,edx
jc WFF_StatusDenied
WFF_StatusApplyOriginal:
pop rax
popfq
mov [rsp+20],r9d
jmp WFF_StatusApply+5
WFF_StatusDenied:
pop rax
popfq
ret
align 10
WFF_StatusCFG:
db 00 00 00 00 00
align 4
WFF_StatusCalls:
dd 0
WFF_StatusTick:
jmp WFF_StatusCode
nop
WFF_StatusApply:
jmp WFF_StatusApplyCode
[DISABLE]
WFF_StatusTick:
db 85 87 B0 2A 00 00
WFF_StatusApply:
db 44 89 4C 24 20
unregistersymbol(WFF_StatusTick)
unregistersymbol(WFF_StatusApply)
unregistersymbol(WFF_StatusCFG)
unregistersymbol(WFF_StatusCalls)
dealloc(WFF_StatusCode)
'''
