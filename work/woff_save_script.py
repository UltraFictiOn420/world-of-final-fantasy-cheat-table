"""Original field-menu Save permission bypass; no save writer modification."""
SAVE = r'''// Shared define must be available during both enable AND disable assembly.
define(WFF_SaveDescriptor,WOFF.exe+2B02278)
[ENABLE]
// The native field-menu descriptor for entry 9 (Save, menu type 0B).
// Its +20 field requires event flag 0FAC. -1 means no required flag,
// exactly as used by the other unrestricted menu entries.
// Changes only this static descriptor, not the persistent event-flag store.
assert(WFF_SaveDescriptor+10,0B 00 00 00 00 00 00 00 FF FF FF FF FF FF FF FF AC 0F 00 00 00 00 00 00)
WFF_SaveDescriptor+20:
dd FFFFFFFF
[DISABLE]
WFF_SaveDescriptor+20:
dd 00000FAC
'''
