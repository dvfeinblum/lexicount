import ast
from bs4 import BeautifulSoup
import re
from redis import StrictRedis
from requests import get

BLOG_FEED_URL = 'http://avagadbro.blogspot.com/feeds/posts/default'

# Some useful constants for parsing blog html
POST_PREFIX_REGEX = "^http://avagadbro.blogspot.com/2"
POST_URL_REL = "alternate"
POST_BODY_CLASS = 'post-body entry-content'

# Redis setup
client = StrictRedis()
LINKS_KEY = 'blog_links'


def get_blogpost_links():
    """
    This goes to the RSS for the blog and fetches a URL from each post
    :return: Array of URLs
    """
    soup = BeautifulSoup(get(BLOG_FEED_URL).content,
                         features='html.parser')
    links = [l.attrs['href'] for l in soup.findAll('link', attrs={'href': re.compile(POST_PREFIX_REGEX),
                                                                  'rel': POST_URL_REL})]

    client.set(LINKS_KEY, links)

    return links


def parse_blog_post(blog_link):
    """
    Given a blog post's URL, this function GETs it and pulls the body out
    :param blog_link: String
    :return: Raw text from the blog post w/html tags
    """
    soup = BeautifulSoup(get(blog_link).content,
                         features='html.parser')
    return soup.find('div', attrs={'class': POST_BODY_CLASS})


if __name__ == "__main__":
    blog_links = client.get(LINKS_KEY)
    if blog_links is None:
        print('Link cache is currently empty. Scraping blog feed at {}'.format(BLOG_FEED_URL))
        blog_links = get_blogpost_links()
    else:
        print('Link cache was hit.')
        blog_links = ast.literal_eval(blog_links.decode('utf-8'))

    for link in blog_links:
        print(parse_blog_post(link))
