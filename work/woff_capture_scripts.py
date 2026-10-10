"""Original capture hooks, derived from live native code and object checks."""

EASY_CAPTURE=r'''[ENABLE]
aobscanmodule(WFF_CaptureReady,WOFF.exe,33 C0 0F 57 C0 0F 2F 41 10 0F 92 C0 89 02 48 8B C2 C3)
aobscanmodule(WFF_CaptureChance,WOFF.exe,F3 0F 10 BB E8 34 00 00 F3 0F 58 BB 48 2B 00 00 0F 2F FE 76 7C)
assert(WFF_CaptureReady,33 C0 0F 57 C0)
assert(WFF_CaptureChance,F3 0F 10 BB E8 34 00 00)
alloc(WFF_CaptureCode,512,WFF_CaptureReady)
label(WFF_ReadyNative)
label(WFF_ChanceCode)
label(WFF_ChanceNative)
label(WFF_ChanceDone)
label(WFF_CapturePercent)
registersymbol(WFF_CaptureReady)
registersymbol(WFF_CaptureChance)

WFF_CaptureCode:
// Readiness method: RCX is the capture component; +8 is its actor.
pushfq
push r8
push r9
mov r8,[rcx+8]
test r8,r8
je WFF_ReadyNative
mov r9,WOFF.exe+2F39FC0
cmp [r8],r9
jne WFF_ReadyNative
cmp dword ptr [r8+2E34],1
jne WFF_ReadyNative
cmp dword ptr [r8+2B40],0
jle WFF_ReadyNative
pop r9
pop r8
popfq
// Native caller still checks target eligibility / required Prism separately.
xor eax,eax
xorps xmm0,xmm0
mov al,1
jmp WFF_CaptureReady+C
WFF_ReadyNative:
pop r9
pop r8
popfq
xor eax,eax
xorps xmm0,xmm0
jmp WFF_CaptureReady+5

WFF_ChanceCode:
// This executes only AFTER the native eligibility check passed.
pushfq
push rax
mov rax,WOFF.exe+2F39FC0
cmp [rbx],rax
jne WFF_ChanceNative
cmp dword ptr [rbx+2E34],1
jne WFF_ChanceNative
cmp dword ptr [rbx+2B40],0
jle WFF_ChanceNative
movss xmm7,[WFF_CapturePercent]
jmp WFF_ChanceDone
WFF_ChanceNative:
movss xmm7,[rbx+34E8]
WFF_ChanceDone:
pop rax
popfq
jmp WFF_CaptureChance+8
align 10
WFF_CapturePercent:
dd (float)100.0

WFF_CaptureReady:
jmp WFF_CaptureCode
WFF_CaptureChance:
jmp WFF_ChanceCode
nop 3

[DISABLE]
WFF_CaptureReady:
db 33 C0 0F 57 C0
WFF_CaptureChance:
db F3 0F 10 BB E8 34 00 00
unregistersymbol(WFF_CaptureReady)
unregistersymbol(WFF_CaptureChance)
dealloc(WFF_CaptureCode)
'''

# Native eligibility has a separate boolean meaning "check required Prism".
# Override that boolean, not the result of the entire eligibility function.
NO_PRISMS = r'''[ENABLE]
aobscanmodule(WFF_PrismEligibility,WOFF.exe,44 89 44 24 18 53 56 57 48 83 EC 30 33 F6 48 8B DA 89 74 24 50 48 8B F9)
aobscanmodule(WFF_PrismConsume,WOFF.exe,39 BE 74 2B 00 00 74 78 48 8B 05 A9 B0 1F 03 44 8B C7)
assert(WFF_PrismEligibility,44 89 44 24 18)
assert(WFF_PrismConsume,39 BE 74 2B 00 00)
alloc(WFF_PrismCode,512,WFF_PrismEligibility)
label(WFF_PrismNative)
label(WFF_PrismConsumeCode)
label(WFF_PrismConsumeNative)
registersymbol(WFF_PrismEligibility)
registersymbol(WFF_PrismConsume)

WFF_PrismCode:
pushfq
push rax
mov rax,WOFF.exe+2F39FC0
cmp [rcx],rax
jne WFF_PrismNative
cmp dword ptr [rcx+2E34],1
jne WFF_PrismNative
cmp dword ptr [rcx+2B40],0
jle WFF_PrismNative
pop rax
popfq
// Retain native living-target, capture-state, and battle eligibility checks.
mov dword ptr [rsp+18],0
jmp WFF_PrismEligibility+5
WFF_PrismNative:
pop rax
popfq
mov [rsp+18],r8d
jmp WFF_PrismEligibility+5

WFF_PrismConsumeCode:
pushfq
push rax
mov rax,WOFF.exe+2F39FC0
cmp [rsi],rax
jne WFF_PrismConsumeNative
cmp dword ptr [rsi+2E34],1
jne WFF_PrismConsumeNative
cmp dword ptr [rsi+2B40],0
jle WFF_PrismConsumeNative
pop rax
popfq
// Capture-specific cleanup only: skip both normal and special Prism deduction.
// Ownership bookkeeping before this point and battle cleanup after it remain.
jmp WFF_PrismConsume+A2
WFF_PrismConsumeNative:
pop rax
popfq
cmp [rsi+2B74],edi
jmp WFF_PrismConsume+6

WFF_PrismEligibility:
jmp WFF_PrismCode
WFF_PrismConsume:
jmp WFF_PrismConsumeCode
nop

[DISABLE]
WFF_PrismEligibility:
db 44 89 44 24 18
WFF_PrismConsume:
db 39 BE 74 2B 00 00
unregistersymbol(WFF_PrismEligibility)
unregistersymbol(WFF_PrismConsume)
dealloc(WFF_PrismCode)
'''

def easy_capture_script():
    """One user toggle owns both readiness/chance and Prism-bypass hooks."""
    ready_enable, ready_disable = EASY_CAPTURE.split('[DISABLE]', 1)
    prism_enable, prism_disable = NO_PRISMS.split('[DISABLE]', 1)
    return (ready_enable + prism_enable.replace('[ENABLE]', '', 1)
            + '\n[DISABLE]\n' + ready_disable + prism_disable)
