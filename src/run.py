from bs4 import BeautifulSoup
import re
from redis import StrictRedis
from requests import get

BLOG_FEED_URL = 'http://avagadbro.blogspot.com/feeds/posts/default'

# Some useful regex
POST_PREFIX = "^http://avagadbro.blogspot.com/2"
REL = "^alternate"

client = StrictRedis()


def get_blogpost_links():
    blog_contents = get(BLOG_FEED_URL).content
    soup = BeautifulSoup(blog_contents,
                         features="html.parser")
    return [link.attrs['href'] for link in soup.findAll('link', attrs={'href': re.compile(POST_PREFIX),
                                                                       'rel': re.compile(REL)})]


if __name__ == "__main__":
    print(get_blogpost_links())
