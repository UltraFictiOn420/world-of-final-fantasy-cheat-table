"""Structural and live read-only checks; never enables cheats or changes memory."""
import argparse
import re
import sys
import xml.etree.ElementTree as E
from pathlib import Path
import unittest
import math


ROOT=Path(__file__).resolve().parents[1]
TABLE=ROOT/"outputs"/"World of Final Fantasy - Original v13.CT"


class TableChecks(unittest.TestCase):
    def test_cleanup_and_information_guards(self):
        entries={e.findtext('ID'):e for e in E.parse(TABLE).findall('.//CheatEntry')}
        for ident in ('83','84','85'):
            self.assertEqual(entries[ident].findtext('Color'),'808080')
            self.assertIn('INFO ONLY',entries[ident].findtext('Description'))
        master=entries['1'].findtext('AssemblerScript')
        self.assertIn('r.OnActivate=function',master)
        self.assertIn('if before then return false end',master)
        self.assertIn('state.records[record.ID]',master)
        self.assertIn('parent.ID==80',master)
        self.assertIn("'OnValueChange'",master)
        self.assertNotIn('LuaScript',[e.tag for e in E.parse(TABLE).getroot()])
        for e in entries.values():
            self.assertNotIn('[Test',e.findtext('Description'))
            self.assertNotIn('; Test',e.findtext('Description'))
        self.assertFalse({'900','901','902'} & set(entries))

    def test_table_parses_and_ids_are_unique(self):
        entries=E.parse(TABLE).findall(".//CheatEntry")
        ids=[e.findtext("ID") for e in entries]
        self.assertEqual(len(ids),len(set(ids)))
        self.assertEqual(set(ids),{"1","10","11","20","21","30","31","32","40","41","42","43","44","45","50","51","60","61","62","70","80","81","82","83","84","85","90"})

    def test_field_save_scope_and_restore(self):
        entries={e.findtext('ID'):e for e in E.parse(TABLE).findall('.//CheatEntry')}
        script=entries['90'].findtext('AssemblerScript')
        self.assertIn('0x5B9B7E76',script)
        self.assertIn('WOFF.exe+2B02278',script)
        self.assertLess(script.index('define(WFF_SaveDescriptor,'),script.index('[ENABLE]'))
        self.assertIn('AC 0F 00 00',script)
        self.assertIn('WFF_SaveDescriptor+20:\ndd FFFFFFFF',script)
        self.assertIn('[DISABLE]\nWFF_SaveDescriptor+20:\ndd 00000FAC',script)
        self.assertNotIn('alloc(',script)
        self.assertNotIn('call ',script)

    def test_replacement_scope_one_shot_and_no_source_writes(self):
        entries={e.findtext('ID'):e for e in E.parse(TABLE).findall('.//CheatEntry')}
        script=entries['80'].findtext('AssemblerScript')
        self.assertIn('mov r10,WOFF.exe+5A0D0F',script)
        self.assertIn('cmp [rsp+70],r10',script)
        self.assertIn('cmp dword ptr [rsi+2E34],1',script)
        self.assertIn('lock cmpxchg [WFF_NextCaptureArmed],ecx',script)
        self.assertIn('mov dword ptr [WFF_NextCaptureArmed],2',script)
        self.assertIn('mov r10,WOFF.exe+734FC7',script)
        self.assertIn('cmp [rsp+28],r10',script)
        self.assertIn('cmp edx,[WFF_LastCaptureSourceID]',script)
        self.assertIn('mov edx,r11d',script)
        self.assertNotIn('mov r8d,r11d',script)
        self.assertNotIn('WFF_ClonePost',script)
        self.assertIn('db 44 8B C0 48 8D 54 24 58',script)
        self.assertIn('db 48 89 5C 24 08',script)
        self.assertNotRegex(script,r'mov\s+(?:dword ptr )?\[(?:rsi|r14|rcx)\+')
        self.assertNotIn('@COUNT@',script)
        self.assertNotIn('@ALLOWLIST@',script)
        self.assertIn('WFF_NextCaptureArmed:\ndd 0',script)
        self.assertEqual(entries['81'].find('DropDownList').attrib['ReadOnly'],'1')
        choices=entries['81'].findtext('DropDownList').splitlines()
        self.assertEqual(len(choices),265)
        self.assertEqual(len({row.split(':',1)[0] for row in choices}),265)
        self.assertTrue(any('EXPERIMENTAL' in row for row in choices))
        self.assertFalse(any(e.findtext('ID') in ('900','901') for e in entries.values()))

    def test_replacement_stack_marker_offsets(self):
        native_frame=0x48
        pushes=5*8
        self.assertEqual(native_frame+pushes,0x70)
        self.assertEqual(0x60+pushes,0x88)
        self.assertEqual(0x68+pushes,0x90)
        self.assertEqual(0x20+pushes,0x48)
        self.assertEqual(0x60+8,0x68)  # post-hook pushes only flags

    def test_prism_bypass_is_capture_scoped(self):
        script=next(e.findtext('AssemblerScript') for e in E.parse(TABLE).findall('.//CheatEntry') if e.findtext('ID')=='70')
        self.assertEqual(script.count('aobscanmodule('),4)
        self.assertEqual(script.count('[ENABLE]'),1)
        self.assertEqual(script.count('[DISABLE]'),1)
        self.assertIn('mov dword ptr [rsp+18],0',script)
        self.assertIn('mov [rsp+18],r8d',script)
        self.assertIn('jmp WFF_PrismConsume+A2',script)
        self.assertIn('cmp dword ptr [rcx+2B40],0',script)
        self.assertIn('cmp dword ptr [rsi+2E34],1',script)
        self.assertIn('db 44 89 44 24 18',script)
        self.assertIn('db 39 BE 74 2B 00 00',script)
        self.assertNotIn('586840:',script)
        self.assertNotRegex(script,r'mov\s+(?:dword ptr )?\[(?:rcx|rsi)\+')

    def test_capture_guards_and_no_actor_writes(self):
        script=next(e.findtext('AssemblerScript') for e in E.parse(TABLE).findall('.//CheatEntry') if e.findtext('ID')=='70')
        self.assertEqual(script.count('aobscanmodule('),4)
        self.assertIn('jmp WFF_CaptureReady+C',script)
        self.assertIn('db 33 C0 0F 57 C0',script)
        self.assertIn('db F3 0F 10 BB E8 34 00 00',script)
        self.assertIn('cmp dword ptr [r8+2B40],0',script)
        self.assertIn('cmp dword ptr [rbx+2E34],1',script)
        self.assertNotRegex(script,r'mov(?:ss)?\s+(?:dword ptr )?\[(?:rcx|r8|rbx)\+')

    def test_cost_and_consumption_hooks(self):
        entries={e.findtext('ID'):e.findtext('AssemblerScript') or '' for e in E.parse(TABLE).findall('.//CheatEntry')}
        self.assertIn('cmp dword ptr [rcx+484],0',entries['51'])
        self.assertIn('cmp [rcx-29B0],rax',entries['51'])
        self.assertEqual(entries['51'].count('aobscanmodule('),4)
        self.assertEqual(entries['60'].count('aobscanmodule('),3)
        self.assertEqual(entries['60'].count('pushfq'),3)
        self.assertEqual(entries['60'].count('popfq'),3)
        for ident in ('61','62'):
            self.assertNotIn('alloc',entries[ident])

    def test_consumption_model(self):
        def consume(count,amount,infinite=False,keep_one=False):
            if count<amount: return 0,False  # Native bulk-removal failure clears the slot.
            remaining=count-amount
            if amount>0:
                if infinite: remaining=count
                elif keep_one: remaining=max(1,remaining)
            return remaining,True
        self.assertEqual(consume(5,1), (4,True))
        self.assertEqual(consume(5,1,True), (5,True))
        self.assertEqual(consume(5,1,False,True), (4,True))
        self.assertEqual(consume(1,1,False,True), (1,True))
        self.assertEqual(consume(0,1,True,True), (0,False))
        self.assertEqual(consume(5,5,False,True), (1,True))
        self.assertEqual(consume(5,-2,True,True), (7,True))
        self.assertEqual(consume(5,1,True,True), (5,True))

    def test_damage_and_vitals_guards(self):
        entries={e.findtext('ID'):e.findtext('AssemblerScript') or '' for e in E.parse(TABLE).findall('.//CheatEntry')}
        self.assertIn('cmp dword ptr [rbx+2E34],1',entries['40'])
        self.assertIn('dq (double)1.0',entries['40'])
        self.assertIn('jp WFF_HPDone',entries['40'])
        self.assertIn('hp>0',entries['42'])
        self.assertIn('readQword(a)==actor.vtable and readInteger(a+0x2E34)==0',entries['42'])
        self.assertIn('getOpenedProcessID()~=pid',entries['42'])

    def test_damage_boundary_model(self):
        def damage(raw,factor=1,side=1,god=False,max_vitals=False,onehit=False,max_hp=152):
            if raw<=0 or side not in (0,1): return raw
            if side==0 and (god or max_vitals): return 0
            value=max_hp if side==1 and onehit else raw*factor
            if math.isnan(value): return raw
            return int(max(0,min(2147483000,value)))
        self.assertEqual(damage(10,0),0)
        self.assertEqual(damage(10,1),10)
        self.assertEqual(damage(10,10),100)
        self.assertEqual(damage(-10,100),-10)
        self.assertEqual(damage(0,100,onehit=True),0)
        self.assertEqual(damage(10,0,onehit=True),152)
        self.assertEqual(damage(10,100,side=0,god=True),0)
        self.assertEqual(damage(10,100,side=0,max_vitals=True),0)
        self.assertEqual(damage(10,float('nan')),10)
        self.assertEqual(damage(10,float('inf')),2147483000)
        self.assertEqual(damage(10,-1),0)
        self.assertEqual(damage(10,100,side=-1),10)

    def test_battle_party_guards_and_restore(self):
        entries={e.findtext('ID'):e.findtext('AssemblerScript') or '' for e in E.parse(TABLE).findall('.//CheatEntry')}
        self.assertIn('cmp dword ptr [rbx+2E34],0',entries['40'])
        self.assertIn('test eax,eax\njle WFF_HPDone',entries['40'])
        self.assertIn('db F3 0F 2C C7 66 0F 6E C0',entries['40'])
        self.assertEqual(entries['50'].count('pushfq'),3)
        self.assertEqual(entries['50'].count('popfq'),3)
        self.assertEqual(entries['50'].count('movups [rsp],xmm0'),3)
        self.assertEqual(entries['50'].count('movups xmm0,[rsp]'),3)
        self.assertEqual(entries['50'].count('aobscanmodule('),3)

    def test_sp_options_share_config_without_duplicate_patches(self):
        tree=E.parse(TABLE)
        children={e.findtext("ID"):e.findtext("AssemblerScript") for e in tree.findall(".//CheatEntry")}
        self.assertIn("WFF_CFG+0:",children["20"])
        self.assertIn("WFF_CFG+1:",children["21"])
        self.assertNotIn("alloc",children["20"])
        self.assertNotIn("alloc",children["21"])

    def test_xp_does_not_rewrite_reward_record(self):
        source=next(e.findtext("AssemblerScript") for e in E.parse(TABLE).findall(".//CheatEntry")
                    if e.findtext("ID")=="30")
        self.assertNotRegex(source,r"(?i)mov\s+\[rbx\+4\]")
        self.assertIn("dq (double)1.0",source)
        self.assertIn("mulsd xmm0,[WFF_XPFactor]",source)
        self.assertIn("mov esi,eax",source)
        self.assertIn("movups [rsp],xmm0",source)
        self.assertIn("movups xmm0,[rsp]",source)
        self.assertIn("ucomisd xmm0,xmm1\nmovups xmm1,[rsp]\nlea rsp,[rsp+10]\npop rax\njae",source)

    def test_no_auto_execution_on_load(self):
        self.assertIsNone(E.parse(TABLE).getroot().find("LuaScript"))

    def test_no_process_handle_reset_during_assembly(self):
        source=E.parse(TABLE).findtext('.//CheatEntry/AssemblerScript')
        self.assertNotIn("openProcess(",source)

    def test_xp_boundary_model(self):
        # Mirrors the intended double-intermediate/recipient-cap algorithm.
        # This is a arithmetic model, not a substitute for in-game testing.
        def award(current,gain,cap,factor=1.0,max_level=False):
            if gain==0: return min(current,cap)
            if max_level: return cap
            scaled=gain*factor
            if math.isnan(scaled): scaled=gain
            if scaled>=cap-current: return cap
            if scaled<0: return min(current,cap)
            return min(cap,current+int(scaled))
        self.assertEqual(award(10,5,100,0),10)
        self.assertEqual(award(10,5,100,1),15)
        self.assertEqual(award(0,1,2000000,50000),50000)
        self.assertEqual(award(0,1,2000000,50000,True),2000000)
        self.assertEqual(award(10,0,100,50000,True),10)
        self.assertEqual(award(1000000,1000000,2000000,50000),2000000)
        self.assertEqual(award(0,2147483647,4000000000,50000),4000000000)
        self.assertEqual(award(10,5,100,float('inf')),100)
        self.assertEqual(award(10,5,100,float('nan')),15)
        self.assertEqual(award(10,5,100,-1),10)


def live_check(pid,exe,gil):
    import pefile
    from ue3_inspect import ProcessMemory
    memory=ProcessMemory(pid)
    try:
        pe=pefile.PE(exe)
        base=pe.OPTIONAL_HEADER.ImageBase
        assert pe.FILE_HEADER.TimeDateStamp==0x5B9B7E76
        text_section=next(s for s in pe.sections if s.Name.startswith(b".text"))
        code=memory.read(base+text_section.VirtualAddress,text_section.Misc_VirtualSize)
        for e in E.parse(TABLE).findall(".//CheatEntry"):
            source=e.findtext("AssemblerScript") or ""
            for name,signature in re.findall(r"aobscanmodule\(([^,]+),WOFF\.exe,([^\)]+)\)",source):
                pattern=b"".join(b"." if token=="??" else re.escape(bytes([int(token,16)]))
                                 for token in signature.split())
                hits=[m.start() for m in re.finditer(pattern,code,re.DOTALL)]
                assert len(hits)==1,(name,hits)
                print(f"Unique live hook: {name} at {base+text_section.VirtualAddress+hits[0]:X}")
        root=int.from_bytes(memory.read(base+0x3439EC0,8),"little")
        observed=memory.u32(root+0x37368)
        assert observed==gil,(observed,gil)
        print(f"Live Gil pointer agrees with screen: {observed}")
        print("Read-only checks passed; no game memory was written.")
    finally:
        memory.close()


if __name__=="__main__":
    if "--pid" in sys.argv:
        parser=argparse.ArgumentParser()
        parser.add_argument("--pid",type=int,required=True)
        parser.add_argument("--exe",required=True)
        parser.add_argument("--gil",type=int,required=True)
        args=parser.parse_args()
        live_check(args.pid,args.exe,args.gil)
    else:
        unittest.main()
