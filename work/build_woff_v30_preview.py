"""Preserve v29; generate a separate preview with only capture changes."""
from pathlib import Path
import sys
import xml.etree.ElementTree as E
from woff_multicapture_replacement import replacement_script

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / 'outputs' / 'World of Final Fantasy - Original v29.CT'
TARGET = ROOT / 'outputs' / 'World of Final Fantasy - Original v30 Preview.CT'

ARM = r'''[ENABLE]
{$lua}
if syntaxcheck then return end
assert(readInteger('WFF_NamingPrepared')==0,
       'Finish all results, then disable/re-enable the replacement parent for a new battle.')
local id=readInteger('WFF_NextCaptureID')
assert(id and id~=0,'Choose a replacement Mirage first.')
{$asm}
WFF_NextCaptureArmed:
dd 1
[DISABLE]
WFF_NextCaptureArmed:
dd 0
'''


def build(preview=True):
    target = TARGET if preview else ROOT / 'outputs' / 'World of Final Fantasy - Original v30.CT'
    title = 'World of Final Fantasy - Original v30' + (' Preview' if preview else '')
    tree = E.parse(SOURCE)
    root = tree.getroot()
    records = {int(e.findtext('ID')): e for e in root.iter('CheatEntry')}
    records[1].find('Description').text = f'"{title} [Enable First]"'
    previous = records[80].findtext('AssemblerScript')
    guard = previous[len('[ENABLE]'):previous.index('aobscanmodule')]
    records[80].find('AssemblerScript').text = replacement_script().replace(
        '[ENABLE]', '[ENABLE]' + guard, 1)
    records[80].find('Description').text = (
        '"Capture Replacement - Enable"')
    records[81].find('Description').text = '"1. Select replacement Mirage in the dropdown menu --->"'
    records[82].find('AssemblerScript').text = ARM
    records[82].find('Description').text = (
        '"2. Leave this on while you wish to replace Mirage replacements"')
    records[30].find('Description').text = '"XP Options - Enable [XP/Levels update once fully out of the battle]"'
    records[90].find('Description').text = '"Save Anywhere - Field Menu"'
    records[207].find('Description').text = '"Features still in testing, but not implemented"'
    records[83].find('Address').text = 'WFF_NamingPrepared'
    records[83].find('Description').text = '"INFO ONLY - Batch preparation [Read-only]"'
    records[83].find('DropDownList').text = (
        '0:Collecting captures\n1:Results prepared - finish naming\n'
        '2:List mismatch - owned results not replaced')
    root.find('Comments').text = (
        title + ('. Not a final release.\n\n' if preview else '. Capture replacement update.\n\n') +
        'All other game scripts and Mirage dropdown choices are unchanged from v29. '
        'Attach CE to the verified WOFF.exe build, enable the top entry, then feature parents.\n\n'
        'MULTI-CAPTURE: Enable the replacement parent before the first capture. Select a '
        'Mirage, then enable "2. Leave this on while you wish to replace Mirage replacements". '
        'Change the dropdown BEFORE each Imprism if you '
        'want different replacements. Each capture snapshots the selection separately; '
        'later choices do not overwrite earlier captures. '
        'Do not disable the parent, reload the table, or close CE during the battle/results. '
        'Complete ALL confirmation and naming screens. In the FIELD, disable/re-enable '
        'the replacement parent before selecting and arming another battle. This version handles only '
        'ONE battle per parent enable; it does not auto-reset across battles.\n\n'
        'CONFIRMED: A three-Mandragora battle produced three Chocochick capture animations, '
        'confirmation appearances, default names and owned Mirage entries. Queue/list '
        'validation passed for all three. User also confirmed the three replacements '
        'retained correct species, names and Mirage Boards after save/reload. A second '
        'three-Mandragora battle, with the dropdown changed before each capture, produced '
        'Chocochick, Mu and Mini Golem: all animations, confirmation/naming screens and '
        'owned species were confirmed, and all three retained their correct species '
        'after saving and reloading. In a mixed-enemy fight, Copper Gnome -> Chocochick '
        'and Floating Eye -> Mu also had correct animations, confirmation/naming screens '
        'and owned entries. Defeating another enemy did not add a capture entry. '
        'Save/reload of that mixed-source pair, full storage and cancellation are not '
        'yet verified. Champion costs remain untested without champions.\n\n'
        'SAFETY: Have room for every capture. Use a separate save slot. Unusual/hidden '
        'dropdown entries remain unverified; normally obtainable does not guarantee safe '
        'replacement. On a list mismatch, owned IDs are not replaced, but prior capture '
        'animations may already have shown selected species. Check your Mirage list.\n\n'
        'SAVE ANYWHERE: Reopen the field menu after toggling. Use a separate save slot.\n\n'
        'XP and level changes appear after battle on the field. 0 = none, 1 = normal. '
        'Grey INFO rows are read-only, not toggles. No temporary trace or diagnostic hook '
        'is included in this file. Saved v29 remains available as a fallback.')
    # Preserve every unrelated gameplay script exactly, not merely equivalent bytes.
    source = {int(e.findtext('ID')): e for e in E.parse(SOURCE).getroot().iter('CheatEntry')}
    for ident, entry in records.items():
        if ident not in {80, 82}:
            assert entry.findtext('AssemblerScript') == source[ident].findtext('AssemblerScript')
    assert not any(int(e.findtext('ID')) >= 900 for e in root.iter('CheatEntry'))
    assert 'WFF_Debug' not in E.tostring(root, encoding='unicode')
    tree.write(target, encoding='utf-8', xml_declaration=True)
    print(target)


if __name__ == '__main__':
    build(preview='--release' not in sys.argv)
