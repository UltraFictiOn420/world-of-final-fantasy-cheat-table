"""Original defeated-enemy loot-roll hook; no global RNG or inventory edits."""
LOOT = r'''[ENABLE]
// Caller is the ordinary defeated-enemy drop loop. Earlier native checks
// require a loot-eligible defeated actor, valid item ID, and positive rate.
aobscanmodule(WFF_LootRoll,WOFF.exe,0F 2F F0 0F 83 F6 01 00 00 48 8B EE 49 8B CD)
assert(WFF_LootRoll,0F 2F F0 0F 83 F6 01 00 00)
// Bypass the first-success exclusion only inside this defeated-enemy loop.
// The following null, invalid-ID and positive-chance guards remain native.
aobscanmodule(WFF_LootAlternatives,WOFF.exe,85 C0 0F 84 6F 02 00 00 48 85 FF 0F 84 66 02 00 00)
assert(WFF_LootAlternatives+2,0F 84 6F 02 00 00)
registersymbol(WFF_LootAlternatives)
alloc(WFF_LootCode,256,WFF_LootRoll)
label(WFF_LootReturn)
label(WFF_LootHits)
registersymbol(WFF_LootRoll)
registersymbol(WFF_LootHits)
WFF_LootCode:
pushfq
lock inc dword ptr [WFF_LootHits]
popfq
// Preserve the native comparison flags; bypass only its failure branch.
comiss xmm6,xmm0
jmp WFF_LootReturn
align 10
WFF_LootHits:
dd 0
WFF_LootRoll:
jmp WFF_LootCode
nop 4
WFF_LootReturn:
WFF_LootAlternatives+2:
nop 6
[DISABLE]
WFF_LootAlternatives+2:
db 0F 84 6F 02 00 00
unregistersymbol(WFF_LootAlternatives)
WFF_LootRoll:
db 0F 2F F0 0F 83 F6 01 00 00
unregistersymbol(WFF_LootHits)
unregistersymbol(WFF_LootRoll)
dealloc(WFF_LootCode)
'''
