"""Regression checks for our pending prototype; not gameplay verification."""
import unittest
from woff_multicapture_replacement import replacement_script
from woff_multicapture_debug import debug_script


def duplicate(rows, source, clone):
    return any(old_source == source and old_clone == clone
               for old_source, old_clone in rows)


class MultiCaptureChecks(unittest.TestCase):
    def test_reused_animation_pointer_is_not_a_duplicate(self):
        self.assertFalse(duplicate([(100, 200)], 101, 200))

    def test_exact_source_clone_pair_is_duplicate(self):
        self.assertTrue(duplicate([(100, 200)], 100, 200))

    def test_same_source_different_clone_is_not_duplicate(self):
        self.assertFalse(duplicate([(100, 200)], 100, 201))

    def test_assembly_checks_source_before_clone(self):
        script = replacement_script()
        body = script.split('WFF_DedupeLoop:\n', 1)[1].split('WFF_Reserve:\n', 1)[0]
        self.assertIn('cmp [r10+8],rsi\njne WFF_DedupeNext', body)
        self.assertLess(body.index('cmp [r10+8],rsi'), body.index('cmp [r10+10],r14'))

    def test_entire_list_validated_before_apply(self):
        script = replacement_script()
        self.assertLess(script.index('WFF_ValidateLoop:\n'), script.index('WFF_ApplyLoop:\n'))
        self.assertIn('cmp rax,rdx\njne WFF_NamingReject', script)
        self.assertIn('cmp [r10],eax\njne WFF_NamingReject', script)

    def test_does_not_write_enemy_identity(self):
        script = replacement_script()
        self.assertNotIn('mov [rsi+', script)
        self.assertNotIn('call ', script)

    def test_queue_is_bounded(self):
        self.assertIn('cmp ecx,#32\njae WFF_QueueNative', replacement_script())

    def test_successful_easy_imprism_does_not_require_native_permission(self):
        script = replacement_script()
        self.assertNotIn('cmp dword ptr [rsi+2B40],0', script)
        self.assertIn('cmp dword ptr [rsp+88],1\njne WFF_QueueNative', script)
        self.assertIn('cmp dword ptr [rsp+90],1\njne WFF_QueueNative', script)
        self.assertIn('cmp [r14],r10\njne WFF_QueueNative', script)

    def test_compact_debug_reserves_bounded_tail(self):
        script = debug_script()
        self.assertIn('alloc(WFF_ReplacementCode,10000,', script)
        self.assertIn('cmp eax,#256', script)
        self.assertLess(len(script.splitlines()), 600)


if __name__ == '__main__':
    unittest.main()
