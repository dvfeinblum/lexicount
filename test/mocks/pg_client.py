class MockPostgresCursor:
    def __init__(self, query_cache=[]):
        self.query_cache = query_cache

    def execute(self, sql):
        print('Received the following sql: %s' % sql)
        self.query_cache.append(sql)
