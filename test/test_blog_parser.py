from unittest import TestCase, mock

from src.blog_parser import get_results
from test.mocks.redis_client import MockRedis


class TestBlogParser(TestCase):

    @mock.patch('src.blog_parser.word_client', new=MockRedis(cache={'foo': 2, 'bar': 1}))
    @mock.patch('src.blog_parser.blogs_scraped_counter', new=1)
    def test_result_generator(self):
        """
        Test ensures that stats can be calculated, given a functioning redis client
        """
        get_results()
