import unittest

from logstack.purging_dict import PurgingDictionary


class Test(unittest.TestCase):
    def test_dict(self):
        d = PurgingDictionary()
        self.assertEqual(len(d), 0)
        d[1] = 'un'
        d[2] = 'deux'
        d[3] = 'trois'
        self.assertEqual(len(d), 3)
        d[1], d[2]
        d.purge()
        self.assertEqual(len(d), 2)
        self.assertEqual(set(d.iterkeys()), set([1, 2]))
        d.purge()
        self.assertEqual(d, {})
