import os
import sys
from urllib.parse import urlparse
import validators

# To remove punctuation, we use translators
_BASE_TRANSLATOR = '!"#$%&\'()*+,/:;<=>?@[\\]^_`{|}~'
word_translator = str.maketrans('', '', _BASE_TRANSLATOR + '.')
sentence_translator = str.maketrans('', '', _BASE_TRANSLATOR)

# Because ya know
DEBUG_MODE = os.environ.get('DEBUG_MODE')

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

POST_PREFIX_REGEX = '^{uri.scheme}://{uri.netloc}/2'.format(
    uri=urlparse(BLOG_FEED_URL))
POST_URL_REL = "alternate"
POST_BODY_CLASS = 'post-body entry-content'


def sanitize_blogpost(post, translator=word_translator):
    """
    This function removes punctuation, newlines, and double spaces so that
    nltk has a fighting chance of parsing a scraped blogpost.
    :param post: Raw post text from Soup
    :param translator: string translator that cleans up punctuation
    :return: cleaned text from the post body
    """
    return post.replace('\n\n', '\n') \
        .replace('\r', ' ').replace('\n', ' ') \
        .translate(translator) \
        .replace('  ', ' ') \
        .strip() \
        .lower()
