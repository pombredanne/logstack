class PurgingDictionary(dict):
    """Special dictionary that can be purged.

    Calling purge() removes the keys that have not been requested since the
    last call to purge().
    This is useful to remove keys that are not needed anymore, when the keys
    cannot be weakly referenced.
    """
    def __init__(self):
        dict.__init__(self)
        self._seen_keys = set()

    def _mark_seen(self, key):
        self._seen_keys.add(key)

    def __getitem__(self, key):
        self._mark_seen(key)
        return dict.__getitem__(self, key)

    def get(self, key, default=None):
        self._mark_seen(key)
        return dict.get(self, key, default)

    def setdefault(self, key, default=None):
        self._mark_seen(key)
        return dict.setdefault(self, key, default)

    def purge(self):
        """Removes entries that have not been queried since the last call.
        """
        if not self._seen_keys:
            self.clear()
            self._seen_keys = set()
            return

        for k in self.keys():
            if k not in self._seen_keys:
                del self[k]
        self._seen_keys = set()
