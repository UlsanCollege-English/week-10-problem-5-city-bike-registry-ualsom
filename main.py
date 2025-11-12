"""
HW05 — City Bike Registry (Resizing Chaining Map)
"""

class HashMap:
    """Chaining hash map with auto-resize at load factor > 0.75."""

    def __init__(self, m=4):
        self._buckets = [[] for _ in range(m)]
        self._size = 0

    def _hash(self, s):
        """Return simple integer hash for string s."""
        return sum(ord(c) for c in s)

    def _index(self, key, m=None):
        """Return bucket index for key with current or given bucket count."""
        if m is None:
            m = len(self._buckets)
        return self._hash(key) % m

    def __len__(self):
        """Return number of stored pairs."""
        return self._size

    def _resize(self, new_m):
        """Resize to new_m buckets and rehash all pairs."""
        old_buckets = self._buckets
        self._buckets = [[] for _ in range(new_m)]
        self._size = 0
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)  # reuse put, will increment size

    def put(self, key, value):
        """Insert or overwrite. Resize first if load will exceed 0.75."""
        if (self._size + 1) / len(self._buckets) > 0.75:
            self._resize(len(self._buckets) * 2)

        idx = self._index(key)
        bucket = self._buckets[idx]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._size += 1

    def get(self, key):
        """Return value for key or None if missing."""
        idx = self._index(key)
        bucket = self._buckets[idx]
        for k, v in bucket:
            if k == key:
                return v
        return None

    def delete(self, key):
        """Remove key if present. Return True if removed else False."""
        idx = self._index(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._size -= 1
                return True
        return False


if __name__ == "__main__":
    # Optional manual check
    hm = HashMap()
    hm.put("apple", 5)
    hm.put("banana", 7)
    print(hm.get("apple"))  # 5
    print(hm.delete("apple"))  # True
    print(hm.get("apple"))  # None
