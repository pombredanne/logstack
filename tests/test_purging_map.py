import unittest

from logstack.purging_map import PurgingMap
from logstack import StackMap


class Frame(object):
    def __init__(self, *frames, **kw):
        try:
            d, k = kw['s']
        except KeyError:
            pass
        else:
            d[k] = self

        self.f_back = None
        for f in frames:
            f.f_back = self


class TestMaps(unittest.TestCase):
    def test_purgingmap(self):
        d = PurgingMap()
        d.set(1, 2)
        d.set(1, 3)
        self.assertEqual(d.get(1), [2, 3])
        self.assertEqual(d.get(2), [])
        d.set(2, 4)
        self.assertEqual(d.get(2), [4])
        d.filter([2, 3])
        self.assertEqual(d.get(1), [])
        self.assertEqual(d.get(2), [4])
        self.assertEqual(d.get(3), [])

    def test_stackmap(self):
        f = {}
        Frame(Frame(Frame(s=(f, 'bar')),
                    Frame(s=(f, 'baz'))),
              s=(f, 'root'))

        self.assertIs(f['bar'].f_back.f_back, f['root'])

        d = StackMap()
        d.set(f['root'], 'root')
        d.set(f['bar'], 'one')
        self.assertEqual(d.get(f['root']), ['root'])
        self.assertEqual(d.get(f['baz']), [])
        self.assertEqual(d.get(f['bar']), ['one'])
        d.remove(f['root'], 'root')
        d.set(f['bar'], 'two')
        self.assertEqual(d.get(f['root']), [])
        self.assertEqual(d.get(f['bar']), ['one', 'two'])
        d.set(f['baz'], 'three')
        self.assertEqual(d.get(f['bar']), [])
        self.assertEqual(d.get(f['baz']), ['three'])
