"""Original scoped battle experiments, with complete native-byte restoration."""
CRITICAL=r'''[ENABLE]
aobscanmodule(WFF_CritChance,WOFF.exe,89 54 24 10 4C 8B DC 55 53 56 41 56 41 57 49 8D 6B A1)
assert(WFF_CritChance,89 54 24 10 4C 8B DC)
alloc(WFF_CritCode,512,WFF_CritChance)
label(WFF_CritNative)
label(WFF_CritReturn)
registersymbol(WFF_CritChance)
WFF_CritCode:
pushfq
push rax
push r10
// Zero native critical chance means the attack is not critical-capable.
test edx,edx
jle WFF_CritNative
test rcx,rcx
jz WFF_CritNative
mov r10,[rcx+8]
test r10,r10
jz WFF_CritNative
mov rax,WOFF.exe+2F39FC0
cmp [r10],rax
je @f
mov rax,WOFF.exe+2F4B168
cmp [r10],rax
jne WFF_CritNative
@@:
cmp dword ptr [r10+2E34],0
jne WFF_CritNative
pop r10
pop rax
popfq
mov eax,#100
ret
WFF_CritNative:
pop r10
pop rax
popfq
mov [rsp+10],edx
mov r11,rsp
jmp WFF_CritChance+7
WFF_CritChance:
jmp WFF_CritCode
nop 2
[DISABLE]
WFF_CritChance:
db 89 54 24 10 4C 8B DC
unregistersymbol(WFF_CritChance)
dealloc(WFF_CritCode)
'''.replace('label(WFF_CritReturn)\n','')

STACK=r'''[ENABLE]
aobscanmodule(WFF_BalanceSet,WOFF.exe,F3 0F 11 B1 28 2B 00 00 0F 28 74 24 20 48 83 C4 30)
assert(WFF_BalanceSet,F3 0F 11 B1 28 2B 00 00)
alloc(WFF_BalanceCode,256,WFF_BalanceSet)
label(WFF_BalanceNative)
registersymbol(WFF_BalanceSet)
WFF_BalanceCode:
pushfq
push rax
mov rax,WOFF.exe+2F4B168
cmp [rcx],rax
jne WFF_BalanceNative
cmp dword ptr [rcx+2E34],0
jne WFF_BalanceNative
cmp dword ptr [rcx+29C8],0
jle WFF_BalanceNative
// Keep the native stack-balance setter at its own maximum, not a huge constant.
movss xmm6,[rcx+2B2C]
WFF_BalanceNative:
pop rax
popfq
movss [rcx+2B28],xmm6
jmp WFF_BalanceSet+8
WFF_BalanceSet:
jmp WFF_BalanceCode
nop 3
[DISABLE]
WFF_BalanceSet:
db F3 0F 11 B1 28 2B 00 00
unregistersymbol(WFF_BalanceSet)
dealloc(WFF_BalanceCode)
'''
