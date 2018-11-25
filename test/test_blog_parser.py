from unittest import TestCase, mock

from src.blog_parser import get_results, analyze_word
from test.mocks.redis_client import MockRedis
from test.mocks.pg_client import MockPostgresCursor


class TestBlogParser(TestCase):

    @mock.patch('src.blog_parser.word_client', new=MockRedis(cache={'foo': 2, 'bar': 1}))
    @mock.patch('src.blog_parser.blogs_scraped_counter', new=1)
    @mock.patch('src.utils.pg._db_cursor', new=MockPostgresCursor())
    def test_result_generator(self):
        """
        Test ensures that stats can be calculated, given a functioning redis client
        """
        get_results()

    @mock.patch('src.blog_parser.word_client', new=MockRedis(cache={'foo': 2, 'bar': 1}))
    @mock.patch('src.utils.pg._db_cursor', new=MockPostgresCursor())
    def test_word_analyze(self):
        """
        Check that the analyzer runs and doesn't bark at empty strings
        """
        self.assertEqual(analyze_word(
            'foo', 'https://amifired.today'), ('foo', 'NN'))
        self.assertIsNone(analyze_word('', 'https://foo.bar'))
