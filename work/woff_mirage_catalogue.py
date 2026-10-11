"""Read installed CSH definition files; emit research metadata, not game assets.

The big-endian cell matrix is independently decoded. No reference CT is read.
"""
from pathlib import Path
import json
import struct
import zlib

GAME_CSV=Path(r'C:\Program Files (x86)\Steam\steamapps\common\WOFF\resource\finalizedCommon\mithril\system\csv')

def csh_rows(path):
    raw=path.read_bytes()
    marker=raw.index(b'BILZ')
    expected=struct.unpack_from('>I',raw,marker+4)[0]
    data=zlib.decompress(raw[marker+16:])
    if len(data)!=expected: raise ValueError('Unverified compressed length')
    cols,count=struct.unpack_from('>II',data,4)
    if 12+cols*count*8>len(data): raise ValueError('Invalid cell matrix')
    rows=[]
    for row in range(count):
        cells=[]
        for col in range(cols):
            offset,kind=struct.unpack_from('>II',data,12+8*(row*cols+col))
            if kind in (0xA0000000,0xC0000000): value=None
            elif kind==0x40000001: value=struct.unpack_from('>i',data,offset)[0]
            elif kind==0x80000001: value=struct.unpack_from('>f',data,offset)[0]
            elif kind<0x10000000 and offset<len(data):
                end=data.index(b'\0',offset)
                value=data[offset:end].decode('utf-8')
            else: raise ValueError(f'Unknown cell type {kind:X}')
            cells.append(value)
        rows.append(cells)
    return rows

def catalogue():
    chars=csh_rows(GAME_CSV/'character_list.csh')
    library=csh_rows(GAME_CSV/'mirage_library_list.csh')
    names={r[0]:r[6] for r in csh_rows(GAME_CSV/'message/us/character_name.csh') if r[0]}
    library_ids={r[3] for r in library if isinstance(r[3],int)}
    resources={r[0]:r for r in csh_rows(GAME_CSV/'character_resource_list.csh') if isinstance(r[0],int)}
    sizes={r[0]:r[2] for r in csh_rows(GAME_CSV/'character_size.csh') if isinstance(r[0],int)}
    result=[]
    for row in chars:
        ident,key,_,name_key=row[:4]
        if not isinstance(ident,int) or not isinstance(key,str): continue
        name=names.get(name_key) or key
        resource=resources.get(row[94])
        size_native=sizes.get(resource[19]) if resource else None
        size={'S':'S','M':'M','L':'L','LL':'XL','EX':'XL'}.get(size_native,'?')
        monster=key.lower().startswith(('monster','addmonster','exmonster'))
        status='library-listed; ownership untested' if ident in library_ids else 'EXPERIMENTAL: outside Mirage library; ownership unverified'
        if name=='NOT USED': status='UNUSED LABEL: experimental; ownership unverified'
        elif isinstance(row[2],str) and '\u30c6\u30b9\u30c8\u7528' in row[2]:
            status='TEST DEFINITION: experimental; ownership unverified'
        elif not monster and ident not in library_ids:
            status='NON-MIRAGE CHARACTER: not a verified ownership candidate'
        result.append(dict(id=ident,hex_id=f'{ident:04X}',key=key,name=name,
                           library_listed=ident in library_ids,status=status,
                           candidate=monster or ident in library_ids,size=size,size_native=size_native,
                           raw_cells=row))
    return result

if __name__=='__main__':
    records=catalogue()
    out=Path(__file__).with_name('woff-mirage-catalogue.json')
    out.write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf-8')
    print('Character records:',len(records),'Library-listed:',sum(r['library_listed'] for r in records))
    print('Catalogue:',out)
    unusual=[r for r in records if not r['library_listed'] and r['candidate']]
    print('Monster definitions outside library:',len(unusual))
    for r in unusual[:12]:
        print(r['hex_id'],ascii(r['name']),r['key'],r['status'])
