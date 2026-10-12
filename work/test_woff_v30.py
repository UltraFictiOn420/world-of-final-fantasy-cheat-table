"""Release structure checks; runtime observations are recorded separately."""
from pathlib import Path
import unittest
import xml.etree.ElementTree as E

ROOT = Path(__file__).resolve().parent.parent


class ReleaseChecks(unittest.TestCase):
    def setUp(self):
        self.root = E.parse(ROOT / 'outputs' / 'World of Final Fantasy - Original v30.CT').getroot()
        self.rows = {e.findtext('ID'): e for e in self.root.iter('CheatEntry')}
        old = E.parse(ROOT / 'outputs' / 'World of Final Fantasy - Original v29.CT')
        self.old = {e.findtext('ID'): e for e in old.getroot().iter('CheatEntry')}

    def test_unrelated_scripts_and_dropdown_preserved(self):
        self.assertEqual(set(self.rows), set(self.old))
        for ident, row in self.rows.items():
            if ident not in {'80', '82'}:
                self.assertEqual(row.findtext('AssemblerScript'), self.old[ident].findtext('AssemblerScript'), ident)
        self.assertEqual(self.rows['81'].findtext('DropDownList'), self.old['81'].findtext('DropDownList'))
        before = self.old['80'].findtext('AssemblerScript')
        guard = before[len('[ENABLE]'):before.index('aobscanmodule')]
        self.assertIn(guard, self.rows['80'].findtext('AssemblerScript'))

    def test_no_diagnostics_or_autorun(self):
        xml = E.tostring(self.root, encoding='unicode')
        self.assertNotIn('WFF_Debug', xml)
        self.assertIsNone(self.root.find('LuaScript'))
        self.assertTrue(all(int(i) < 900 for i in self.rows))
        for row in self.rows.values():
            text = row.findtext('Description') or ''
            self.assertNotIn('DIAGNOSTIC', text)
            self.assertNotIn('Preview', text)
        for ident in ('83', '84', '85'):
            self.assertEqual(self.rows[ident].findtext('Color'), '808080')

    def test_replacement_and_reset_instructions(self):
        script = self.rows['80'].findtext('AssemblerScript')
        self.assertEqual(script.count('aobscanmodule('), 3)
        self.assertNotIn('cmp dword ptr [rsi+2B40],0', script)
        self.assertIn('WFF_ValidateLoop:', script)
        self.assertIn('WFF_NamingReject:', script)
        self.assertNotIn('@COUNT@', script)
        self.assertNotIn('@ROWS@', script)
        self.assertIn("readInteger('WFF_NamingPrepared')==0", self.rows['82'].findtext('AssemblerScript'))
        comments = self.root.findtext('Comments')
        self.assertIn('ONE battle per parent enable', comments)
        self.assertIn('Change the dropdown BEFORE each Imprism', comments)
        self.assertIn('full storage and cancellation', comments)

    def test_requested_display_descriptions(self):
        descriptions = {
            '80': 'Capture Replacement - Enable',
            '81': '1. Select replacement Mirage in the dropdown menu --->',
            '82': '2. Leave this on while you wish to replace Mirage replacements',
            '30': 'XP Options - Enable [XP/Levels update once fully out of the battle]',
            '90': 'Save Anywhere - Field Menu',
            '207': 'Features still in testing, but not implemented',
        }
        for ident, text in descriptions.items():
            self.assertEqual(self.rows[ident].findtext('Description'), f'"{text}"')


if __name__ == '__main__':
    unittest.main()
