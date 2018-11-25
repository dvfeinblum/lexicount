from src.utils.pg import _GET_WORD_COUNT_QUERY


class MockPostgresCursor:
    def __init__(self, query_cache=set([])):
        self.query_cache = query_cache

    def execute(self, sql):
        print('Received the following sql: %s' % sql)
        self.query_cache.add(sql)
        if sql == _GET_WORD_COUNT_QUERY:
            return 1
