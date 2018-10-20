class MockRedis:
    def __init__(self, cache=None):
        self.cache = cache

    def incr(self, key):
        self.cache[key] = self.cache.setdefault(key, 0) + 1

    def dbsize(self):
        return len(self.cache)

    def set(self, k, v):
        self.cache[k] = v

    def get(self, k):
        return self.cache.get(k)
