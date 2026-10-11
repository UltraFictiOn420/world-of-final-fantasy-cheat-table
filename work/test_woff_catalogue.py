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

    def test_sizes_from_resources(self):
        for name,size in [('Mu','S'),('Chocochick','S'),('Behemoth','L'),('Ifrit','L'),('Bahamut','XL')]:
            self.assertTrue(any(r['name']==name and r['size']==size for r in self.records))
        self.assertTrue(all(r['size'] in ('S','M','L','XL') for r in self.records if r['candidate']))

    def test_clean_dropdown(self):
        from woff_replacement_options import dropdown,candidates
        text=dropdown()
        self.assertNotIn('Monster',text)
        self.assertNotIn(', ID ',text)
        self.assertIn('Chocochick [S] - Legit Mirage',text)
        self.assertEqual(len(text.splitlines()),len(candidates())+1)

    def test_ownership_is_not_library_membership(self):
        from woff_replacement_options import ownership_status
        self.assertIn('Not normally capturable',ownership_status(self.by_id[7194]))
        self.assertIn('defeat reward',ownership_status(self.by_id[8028]))
        self.assertIn('Save risk unverified',ownership_status(self.by_id[8029]))
        self.assertEqual(ownership_status(self.by_id[7031]),'Legit Mirage')

    def test_unknown_entries_have_no_safety_claim(self):
        from woff_replacement_options import ownership_status,candidates
        for record in candidates():
            status=ownership_status(record)
            self.assertNotIn('Working Mirage',status)
            self.assertNotIn('Bugged',status)

if __name__=='__main__':unittest.main()
