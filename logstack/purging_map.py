class PurgingMap(object):
    """Special mapping that only keeps some keys.

    A key is set, you must specify which keys are able to keep on existing; all
    other keys are dropped.

    Note that this is different from a dict, as one key has a list of values.
    """
    def __init__(self):
        self._dict = {}

    def set(self, key, value):
        """Adds a new value for the key. This does not replace previous values.
        """
        self._dict.setdefault(key, []).append(value)

    def get(self, key):
        """Returns the list of values for that key.
        """
        return self._dict.get(key, [])

    def remove(self, key, value):
        """Removes a specific (key, value) pair.

        Raises KeyError if there is no value for that key, ValueError if value
        is not one of them.
        """
        self._dict[key].remove(value)

    def filter(self, keys):
        """Only keeps specific keys in the map.

        Every key that is not in the iterable keys will be purged.
        """
        if not isinstance(keys, set):
            keys = set(keys)
        for k in self._dict.keys():
            if k not in keys:
                del self._dict[k]
