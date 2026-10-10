"""Original party-only battle hooks for the verified 2.0.0.0 runtime."""

HP = r'''[ENABLE]
aobscanmodule(WFF_HPApply,WOFF.exe,F3 0F 2C C7 66 0F 6E C0 0F 5B C0 F3 0F 5C C8 F3 0F 5F CB)
assert(WFF_HPApply,F3 0F 2C C7 66 0F 6E C0)
alloc(WFF_HPCode,1024,WFF_HPApply)
label(WFF_GodMode)
label(WFF_MaxVitals)
label(WFF_OneHit)
label(WFF_PlayerDamage)
label(WFF_EnemyDamage)
label(WFF_DamageCap)
label(WFF_HPParty)
label(WFF_HPEnemy)
label(WFF_HPScale)
label(WFF_HPZero)
label(WFF_HPCap)
label(WFF_LastHPActor)
label(WFF_HPDone)
registersymbol(WFF_HPApply)
registersymbol(WFF_GodMode)
registersymbol(WFF_MaxVitals)
registersymbol(WFF_OneHit)
registersymbol(WFF_PlayerDamage)
registersymbol(WFF_EnemyDamage)
registersymbol(WFF_LastHPActor)
WFF_HPCode:
cvttss2si eax,xmm7
pushfq
mov [WFF_LastHPActor],rbx
// Only positive HP loss to the independently observed player side is blocked.
test eax,eax
jle WFF_HPDone
cmp dword ptr [rbx+2E34],0
je WFF_HPParty
cmp dword ptr [rbx+2E34],1
je WFF_HPEnemy
jmp WFF_HPDone
WFF_HPParty:
cmp byte ptr [WFF_MaxVitals],0
jne WFF_HPZero
cmp byte ptr [WFF_GodMode],0
jne WFF_HPZero
cvtsi2sd xmm0,eax
mulsd xmm0,[WFF_EnemyDamage]
jmp WFF_HPScale
WFF_HPEnemy:
cmp byte ptr [WFF_OneHit],0
je @f
movss xmm0,[rbx+29CC]
cvtss2sd xmm0,xmm0
jmp WFF_HPScale
@@:
cvtsi2sd xmm0,eax
mulsd xmm0,[WFF_PlayerDamage]
WFF_HPScale:
// NaN falls back to native damage. Negative factors mean zero damage.
ucomisd xmm0,xmm0
jp WFF_HPDone
comisd xmm0,[WFF_DamageCap]
jae WFF_HPCap
cvttsd2si eax,xmm0
test eax,eax
jns WFF_HPDone
WFF_HPZero:
xor eax,eax
jmp WFF_HPDone
WFF_HPCap:
mov eax,#2147483000
WFF_HPDone:
popfq
movd xmm0,eax
jmp WFF_HPApply+8
align 10
WFF_GodMode:
db 00
WFF_MaxVitals:
db 00
WFF_OneHit:
db 00
align 8
WFF_PlayerDamage:
dq (double)1.0
WFF_EnemyDamage:
dq (double)1.0
WFF_DamageCap:
dq (double)2147483000.0
WFF_LastHPActor:
dq 0
WFF_HPApply:
jmp WFF_HPCode
nop 3
[DISABLE]
WFF_HPApply:
db F3 0F 2C C7 66 0F 6E C0
unregistersymbol(WFF_HPApply)
unregistersymbol(WFF_GodMode)
unregistersymbol(WFF_MaxVitals)
unregistersymbol(WFF_OneHit)
unregistersymbol(WFF_PlayerDamage)
unregistersymbol(WFF_EnemyDamage)
unregistersymbol(WFF_LastHPActor)
dealloc(WFF_HPCode)
'''

# Finite battle actor pool, verified class and side before every write. No stale
# pointer is trusted merely because it matched during initial discovery.
MAX_VITALS = r'''[ENABLE]
{$lua}
if syntaxcheck then return end
if WFF_VitalsTimer then error('Max-vitals timer is already active.') end
local pid=getOpenedProcessID()
local classes={getAddress('WOFF.exe+2F4B168'),getAddress('WOFF.exe+2F39FC0')}
local flag=getAddress('WFF_MaxVitals')
local actors={}
for _,vt in ipairs(classes) do
  local bytes={}
  local value=vt
  for i=1,8 do bytes[i]=string.format('%02X',value%256); value=math.floor(value/256) end
  local hits=AOBScan(table.concat(bytes,' '),'+W-C')
  if hits then
    for i=0,hits.Count-1 do
      local a=tonumber(hits[i],16)
      local side=readInteger(a+0x2E34)
      if side==0 or side==-1 or side==0xFFFFFFFF then actors[#actors+1]={address=a,vtable=vt} end
    end
    hits.destroy()
  end
end
if #actors==0 then error('No verified party actor pool found.') end
local function refill()
  if getOpenedProcessID()~=pid then
    if WFF_VitalsTimer then WFF_VitalsTimer.destroy();WFF_VitalsTimer=nil end
    return
  end
  for _,actor in ipairs(actors) do
    local a=actor.address
    if readQword(a)==actor.vtable and readInteger(a+0x2E34)==0 then
      local hp,maxHP=readFloat(a+0x29C8),readFloat(a+0x29CC)
      local maxAP=readFloat(a+0x29D4)
      if hp and maxHP and hp>0 and maxHP>=hp and maxHP<10000000 then
        writeFloat(a+0x29C8,maxHP)
        if maxAP and maxAP>=0 and maxAP<=1000 then writeFloat(a+0x29D0,maxAP) end
      end
    end
  end
end
WFF_VitalsTimer=createTimer(nil,false)
WFF_VitalsTimer.Interval=100
WFF_VitalsTimer.OnTimer=refill
writeBytes(flag,1)
refill()
WFF_VitalsTimer.Enabled=true
{$asm}
[DISABLE]
{$lua}
if syntaxcheck then return end
if WFF_VitalsTimer then WFF_VitalsTimer.destroy();WFF_VitalsTimer=nil end
local flag=getAddressSafe('WFF_MaxVitals')
if flag then writeBytes(flag,0) end
{$asm}
'''


def ap_script():
    # Native AP refill, ability assignment/spending, and AP damage paths.
    paths = [
        ('Regen', 'rdi', 'F3 0F 11 B7 D0 29 00 00 48 8B 0D ?? ?? ?? ?? 48 8B 01 FF 90 40 02 00 00', 'F3 0F 11 B7 D0 29 00 00'),
        ('Set', 'rbx', 'F3 0F 11 B3 D0 29 00 00 0F 28 74 24 30 0F 28 7C 24 20', 'F3 0F 11 B3 D0 29 00 00'),
        ('Damage', 'rbx', 'F3 0F 11 B3 D0 29 00 00 48 8B 5C 24 58 48 8B 74 24 60', 'F3 0F 11 B3 D0 29 00 00'),
    ]
    lines = ['[ENABLE]']
    for name, reg, pattern, original in paths:
        symbol = 'WFF_AP'+name
        lines += [f'aobscanmodule({symbol},WOFF.exe,{pattern})', f'assert({symbol},{original})',
                  f'alloc({symbol}Code,256,{symbol})', f'label({symbol}Original)', f'label({symbol}Done)',
                  f'registersymbol({symbol})', f'{symbol}Code:', 'pushfq',
                  f'cmp dword ptr [{reg}+2E34],0', f'jne {symbol}Original',
                  'sub rsp,10', 'movups [rsp],xmm0', f'movss xmm0,[{reg}+29D4]',
                  f'movss [{reg}+29D0],xmm0', 'movups xmm0,[rsp]', 'add rsp,10',
                  f'jmp {symbol}Done', f'{symbol}Original:', f'movss [{reg}+29D0],xmm6',
                  f'{symbol}Done:', 'popfq', f'jmp {symbol}+8', f'{symbol}:', f'jmp {symbol}Code', 'nop 3']
    lines += ['[DISABLE]']
    for name, reg, pattern, original in paths:
        symbol = 'WFF_AP'+name
        lines += [f'{symbol}:', f'db {original}', f'unregistersymbol({symbol})', f'dealloc({symbol}Code)']
    return '\n'.join(lines)+'\n'
