import ast
from bs4 import BeautifulSoup
import re
from redis import StrictRedis
from requests import get

BLOG_FEED_URL = 'http://avagadbro.blogspot.com/feeds/posts/default'

# Some useful regex for parsing links
POST_PREFIX = "^http://avagadbro.blogspot.com/2"
REL = "^alternate"

# Redis setup
client = StrictRedis()
LINKS_KEY = 'blog_links'


def get_blogpost_links():
    soup = BeautifulSoup(get(BLOG_FEED_URL).content,
                         features='html.parser')
    links = [link.attrs['href'] for link in soup.findAll('link', attrs={'href': re.compile(POST_PREFIX),
                                                                        'rel': re.compile(REL)})]

    client.set(LINKS_KEY, links)
    return links


def parse_blog_post(blog_link):
    resp = get(blog_link)
    print(resp.content)


if __name__ == "__main__":
    blog_links = client.get(LINKS_KEY)
    if blog_links is None:
        print('Link cache is currently empty. Scraping blog feed at {}'.format(BLOG_FEED_URL))
        blog_links = get_blogpost_links()
    else:
        print('Link cache was hit.')
        blog_links = ast.literal_eval(blog_links.decode('utf-8'))

    for link in blog_links:
        parse_blog_post(link)
