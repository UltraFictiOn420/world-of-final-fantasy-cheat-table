"""Read-only checks against the installed character definitions."""
import unittest
from woff_mirage_catalogue import catalogue

class CatalogueChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=catalogue()
        cls.by_id={r['id']:r for r in cls.records}

    def test_unique_ids(self):
        self.assertEqual(len(self.records),len(self.by_id))
        self.assertEqual(len(self.records),355)

    def test_observed_mu(self):
        self.assertEqual(self.by_id[0x1BA1]['name'],'Mu')
        self.assertTrue(self.by_id[0x1BA1]['library_listed'])

    def test_experimental_labels(self):
        self.assertIn('TEST DEFINITION',self.by_id[0x1F5D]['status'])
        self.assertIn('UNUSED LABEL',self.by_id[0x1F61]['status'])
        self.assertTrue(self.by_id[0x1F61]['candidate'])
        self.assertFalse(self.by_id[0]['candidate'])

    def test_library_does_not_imply_safe(self):
        for r in self.records:
            if r['library_listed']:self.assertRegex(r['status'],r'untested|unverified')

if __name__=='__main__':unittest.main()
