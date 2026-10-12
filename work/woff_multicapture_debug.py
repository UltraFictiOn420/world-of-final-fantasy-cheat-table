"""Instrument our prototype without changing its existing decisions.

Snapshots capture-path flags and every early-result preparation, including
the shrinking list's contents. Bounded diagnostic writes only.
"""
from pathlib import Path
from woff_multicapture_replacement import replacement_script


def observation(event):
    name = f'WFF_Debug{event}Exit'
    lines = ['pushfq','push rax','push rcx','push rdx','push r10','push r11']
    if event == 1:
        lines += ['mov r10,WOFF.exe+5A0D0F','cmp [rsp+78],r10',f'jne {name}',
                  'mov r10,WOFF.exe+2F39FC0','cmp [rsi],r10',f'jne {name}',
                  'cmp dword ptr [rsi+2E34],1',f'jne {name}']
    lines += ['mov eax,1','lock xadd [WFF_DebugCount],eax','cmp eax,#256',
              f'jae {name}','shl eax,7','lea r11,[WFF_DebugRows]','add r11,rax',
              f'mov dword ptr [r11],{event}',
              'mov eax,[WFF_CaptureCount]','mov [r11+4],eax',
              'mov eax,[WFF_NextCaptureArmed]','mov [r11+8],eax',
              'mov eax,[WFF_NamingPrepared]','mov [r11+C],eax']
    if event == 1:
        lines += ['mov eax,[rsp+20]','mov [r11+10],eax',
                  'mov eax,[rsi+2B40]','mov [r11+14],eax',
                  'mov eax,[rsp+90]','mov [r11+18],eax',
                  'mov eax,[rsp+98]','mov [r11+1C],eax',
                  'mov [r11+20],rsi','mov [r11+28],r14']
    else:
        lines += ['mov [r11+30],rdi','mov r10,[rdi+800]','mov [r11+38],r10',
                  'mov rdx,[rdi+808]','mov [r11+40],rdx',
                  'mov eax,[rdi+818]','mov [r11+48],eax',
                  'mov eax,[rdi+824]','mov [r11+4C],eax',
                  'test r10,r10',f'jz {name}','cmp rdx,r10',f'jbe {name}',
                  'sub rdx,r10','cmp rdx,#128',f'ja {name}',
                  'xor ecx,ecx',f'WFF_Debug{event}ListLoop:',
                  'cmp ecx,#8',f'jae {name}', 'mov eax,ecx','shl eax,2',
                  'cmp rax,rdx',f'jae {name}',
                  'mov eax,[r10+rcx*4]','mov [r11+50+rcx*4],eax',
                  'inc ecx',f'jmp WFF_Debug{event}ListLoop']
    return '\n'.join(lines+[name+':','pop r11','pop r10','pop rdx','pop rcx',
                            'pop rax','popfq'])+'\n'


def debug_script():
    script = replacement_script().replace(
        'alloc(WFF_ReplacementCode,4000,', 'alloc(WFF_ReplacementCode,10000,')
    labels = ['WFF_DebugCount','WFF_DebugRows','WFF_Debug1Exit','WFF_Debug2Exit',
              'WFF_Debug2ListLoop']
    declarations = '\n'.join(f'label({s})' for s in labels)
    declarations += '\nregistersymbol(WFF_DebugCount)\nregistersymbol(WFF_DebugRows)\n'
    script = script.replace('WFF_ReplacementCode:\n', declarations+
                            '\nWFF_ReplacementCode:\n'+observation(1), 1)
    script = script.replace('WFF_NamingPrepareCode:\n',
                            'WFF_NamingPrepareCode:\n'+observation(2), 1)
    script = script.replace('\nWFF_CloneArgsHook:\n',
        '\nalign 10\nWFF_DebugCount:\ndd 0\nalign 10\nWFF_DebugRows:\n'+
        '// Diagnostic rows occupy the zero-initialized tail of the 64KB allocation.\n'+
        'db 0\nWFF_CloneArgsHook:\n',1)
    script = script.replace('dealloc(WFF_ReplacementCode)',
        'unregistersymbol(WFF_DebugCount)\nunregistersymbol(WFF_DebugRows)\n'+
        'dealloc(WFF_ReplacementCode)')
    return script


if __name__ == '__main__':
    Path(__file__).with_name('woff-multicapture-debug.aa').write_text(
        debug_script(), encoding='utf-8')
