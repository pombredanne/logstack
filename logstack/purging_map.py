class PurgingMap(object):
    """Special mapping that only keeps some keys.

    A key is set, you must specify which keys are able to keep on existing; all
    other keys are dropped.

    Note that this is different from a dict, as one key has a list of values.
    """
    def __init__(self):
        self._dict = {}

    def set(self, key, value):
        self._dict.setdefault(key, []).append(value)

    def get(self, key):
        return self._dict.get(key, [])

    def remove(self, key, value):
        self._dict[key].remove(value)

    def filter(self, keys):
        if not isinstance(keys, set):
            keys = set(keys)
        for k in self._dict.keys():
            if k not in keys:
                del self._dict[k]
