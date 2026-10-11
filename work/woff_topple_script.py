"""Original one-shot enemy stack collapse, dispatched on the game's actor update."""

NATIVE = r'''[ENABLE]
aobscanmodule(WFF_ToppleRead,WOFF.exe,F3 0F 59 BF EC 29 00 00 F3 0F 58 BF D8 29 00 00)
assert(WFF_ToppleRead,F3 0F 59 BF EC 29 00 00)
assert(WOFF.exe+55D440,40 53 55 56 57 41 56 48 83 EC 20 33 DB 48 8B E9)
alloc(WFF_ToppleCode,1024,WFF_ToppleRead)
label(WFF_ToppleRequest)
label(WFF_ToppleSeen)
label(WFF_ToppleCalls)
label(WFF_ToppleNative)
registersymbol(WFF_ToppleRead)
registersymbol(WFF_ToppleRequest)
registersymbol(WFF_ToppleSeen)
registersymbol(WFF_ToppleCalls)
WFF_ToppleCode:
pushfq
push rbx
push rax
mov rax,rdi
test rax,rax
jz WFF_ToppleNative
mov rbx,WOFF.exe+2F4B168
cmp [rax],rbx
jne WFF_ToppleNative
mov rbx,rax
cmp dword ptr [rbx+2E34],1
jne WFF_ToppleNative
cmp dword ptr [rbx+29C8],0
jle WFF_ToppleNative
test byte ptr [rbx+29A8],2
jnz WFF_ToppleNative
mov rbx,[rax+3698]
sub rbx,[rax+3690]
cmp rbx,10
jb WFF_ToppleNative
cmp rbx,18
ja WFF_ToppleNative
inc dword ptr [WFF_ToppleSeen]
cmp dword ptr [WFF_ToppleRequest],1
jne WFF_ToppleNative
mov rbx,[WOFF.exe+3439EE0]
test rbx,rbx
jz WFF_ToppleNative
// Consume BEFORE dispatch; native callbacks cannot trigger a second collapse.
mov dword ptr [WFF_ToppleRequest],0
push rcx
push rdx
push r8
push r9
push r10
push r11
// Native actor update is aligned here. Nine pushes require an extra 8 bytes.
sub rsp,0A8
movups [rsp+40],xmm0
movups [rsp+50],xmm1
movups [rsp+60],xmm2
movups [rsp+70],xmm3
movups [rsp+80],xmm4
movups [rsp+90],xmm5
// Native binding only reads wrapper+8. Use a local view, not actor+34D8:
// that embedded object's +8 is null for observed enemy UnitTower actors.
mov qword ptr [rsp+20],0
mov [rsp+28],rax
lea rcx,[rsp+20]
call WOFF.exe+55D440
inc dword ptr [WFF_ToppleCalls]
movups xmm0,[rsp+40]
movups xmm1,[rsp+50]
movups xmm2,[rsp+60]
movups xmm3,[rsp+70]
movups xmm4,[rsp+80]
movups xmm5,[rsp+90]
add rsp,0A8
pop r11
pop r10
pop r9
pop r8
pop rdx
pop rcx
WFF_ToppleNative:
pop rax
pop rbx
popfq
mulss xmm7,[rdi+29EC]
jmp WFF_ToppleRead+8
align 10
WFF_ToppleRequest:
dd 0
WFF_ToppleSeen:
dd 0
WFF_ToppleCalls:
dd 0
WFF_ToppleRead:
jmp WFF_ToppleCode
nop 3
[DISABLE]
WFF_ToppleRead:
db F3 0F 59 BF EC 29 00 00
unregistersymbol(WFF_ToppleRead)
unregistersymbol(WFF_ToppleRequest)
unregistersymbol(WFF_ToppleSeen)
unregistersymbol(WFF_ToppleCalls)
dealloc(WFF_ToppleCode)
'''

def topple_script():
    # All native calls occur in the actor's native update thread, NEVER a CE timer.
    embedded = NATIVE.replace('[ENABLE]', '__NATIVE_ENABLE__').replace('[DISABLE]', '__NATIVE_DISABLE__')
    return r'''[ENABLE]
{$lua}
if syntaxcheck then return end
assert(getOpenedProcessID()==getProcessIDFromProcessName('WOFF.exe'),'Attach WoFF first')
local b=assert(getAddressSafe('WOFF.exe'),'Start WoFF first')
local pe=assert(readInteger(b+0x3C))
assert(readInteger(b+pe+8)==0x5B9B7E76,'Unverified WoFF build; nothing patched')
assert(not _G.WFFTopple,'Topple is already installed')
local native=[==[''' + embedded + r''']==]
native=native:gsub('__NATIVE_ENABLE__','['..'ENABLE'..']'):gsub('__NATIVE_DISABLE__','['..'DISABLE'..']')
local ok,di=autoAssemble(native)
assert(ok,tostring(di))
local s={native=native,disableInfo=di,pid=getOpenedProcessID(),requested=0}
local installed,err=pcall(function()
 s.hotkey=createHotkey(function()
  if getOpenedProcessID()~=s.pid then return end
  local p=getAddressSafe('WFF_ToppleRequest')
  if not p or readInteger(p)~=0 then return end
  s.requested=getTickCount()
  writeInteger(p,1)
  -- Acknowledges only an accepted request, not a completed collapse.
  if type(beep)=='function' then pcall(beep) end
 end,0x77) -- F8: one enemy stack per press, no HP damage.
 s.hotkey.DelayBetweenActivate=750
 s.timer=createTimer(nil,false)
 s.timer.Interval=100
 s.timer.OnTimer=function()
  if getOpenedProcessID()~=s.pid then return end
  local p=getAddressSafe('WFF_ToppleRequest')
  -- An unconsumed request expires: no stale press waiting for a later battle.
  if p and readInteger(p)==1 and getTickCount()-s.requested>3000 then
   writeInteger(p,0)
  end
 end
 s.timer.Enabled=true
end)
if not installed then
 if s.hotkey then s.hotkey.destroy() end
 if s.timer then s.timer.destroy() end
 autoAssemble(native,false,di)
 error(tostring(err))
end
_G.WFFTopple=s
{$asm}
[DISABLE]
{$lua}
if syntaxcheck then return end
local s=_G.WFFTopple
if not s then return end
if getOpenedProcessID()~=s.pid then error('Reattach original game before disabling Topple') end
writeInteger(getAddress('WFF_ToppleRequest'),0)
local ok,msg=autoAssemble(s.native,false,s.disableInfo)
assert(ok,tostring(msg))
if s.hotkey then s.hotkey.destroy() end
if s.timer then s.timer.destroy() end
_G.WFFTopple=nil
{$asm}
'''
