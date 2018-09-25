import os
import string
import sys
from urllib.parse import urlparse
import validators

# To remove punctuation, we use a translator
translator = str.maketrans('', '', string.punctuation)

# Blog constants
if 'BLOG_FEED_URL' in os.environ:
    feed_url = os.environ['BLOG_FEED_URL']
    if validators.url(feed_url):
        BLOG_FEED_URL = feed_url
    else:
        print('BLOG_FEED_URL envar is not a valid url.')
        sys.exit(1)

else:
    BLOG_FEED_URL = 'http://avagadbro.blogspot.com/feeds/posts/default'

POST_PREFIX_REGEX = '^{uri.scheme}://{uri.netloc}/2'.format(uri=urlparse(BLOG_FEED_URL))


def sanitize_blogpost(post):
    """
    This function removes punctuation, newlines, and double spaces so that
    nltk has a fighting chance of parsing a scraped blogpost.
    :param post:
    :return:
    """
    return post.translate(translator) \
        .replace('\n\n', '\n') \
        .replace('\r', '').replace('\n', '') \
        .replace('  ', ' ') \
        .strip() \
        .lower()