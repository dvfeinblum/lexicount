import ast
from bs4 import BeautifulSoup
import nltk
import re
from redis import StrictRedis
import requests as r
import utils

# Some useful constants for parsing blog html
POST_URL_REL = "alternate"
POST_BODY_CLASS = 'post-body entry-content'

# Redis stuff
WORD_DB_ID = 0
NLTK_DB_ID = 1
word_client = StrictRedis(db=WORD_DB_ID)
nltk_client = StrictRedis(db=NLTK_DB_ID)
LINKS_KEY = 'blog_links'

blogs_scraped_counter = 0
word_count = 0
pos_counts = {}

# Makes for easier debugging when it comes to nltk failures
error_file = open('error.txt', 'w')


def get_blogpost_links():
    """
    This goes to the RSS for the blog and fetches a URL from each post
    :return: Array of URLs
    """
    soup = BeautifulSoup(r.get(utils.BLOG_FEED_URL).content,
                         features='html.parser')
    links = [l.attrs['href'] for l in soup.findAll('link', attrs={'href': re.compile(utils.POST_PREFIX_REGEX),
                                                                  'rel': POST_URL_REL})]
    word_client.set(LINKS_KEY, links)

    return links


def parse_blog_post(blog_link):
    """
    Given a blog post's URL, this function GETs it and pulls the body out
    :param blog_link: String
    :return: Raw text from the blog post w/html tags stripped out
    """
    global blogs_scraped_counter
    global word_count
    global error_file
    print('Fetching raw text for {}'.format(blog_link))
    soup = BeautifulSoup(r.get(blog_link).content,
                         features='html.parser')
    post_text = soup.find('div', attrs={'class': POST_BODY_CLASS}).get_text()

    sanitized_post_text = utils.sanitize_blogpost(post_text)
    print('Successfully parsed post. Updating word counts in redis.')
    if utils.DEBUG_MODE:
        print('\nSanitized blogpost:\n{clean}\n\nOriginal text:{orig}'.format(clean=sanitized_post_text,
                                                                              orig=post_text))
    for word in sanitized_post_text.split(' '):
        # First we hit the word count cache
        word_client.incr(word)
        word_count = word_count + 1

        # Now we do some nltk wizardry
        try:
            pos_array = nltk.pos_tag([word])

            pos_tuple = pos_array[0]
            pos = pos_tuple[1]
            nltk_client.incr(pos)
            if pos in pos_counts:
                pos_counts[pos] = pos_counts[pos] + 1
            else:
                pos_counts[pos] = 1
        except Exception as e:
            print('failed to nltk-ify a post.\nURL: {url}\nException: {e}'.format(e=e, url=blog_link))
            error_file.write('URL: ' + blog_link + '\n' + repr(sanitized_post_text) + '\n')

    blogs_scraped_counter = blogs_scraped_counter + 1


def get_results():
    """
    Once the run is complete, we'll spit out some stats.
    :return:
    """
    # we subtract one because of the blog_links entry
    unique_word_count = word_client.dbsize() - 1
    print('\nRESULTS\n')
    print('Number of words found across all posts: {}'.format(word_count))
    print('Number of unique words found across all posts: {}'.format(unique_word_count))
    print('Number of posts scraped: {}\n'.format(blogs_scraped_counter))
    print('Average repeat-rate of all words: {}'.format(word_count / unique_word_count))
    print('Average words per post: {}'.format(word_count / blogs_scraped_counter))
    print('Unique words per post: {}\n'.format(unique_word_count / blogs_scraped_counter))
    print('Part of Speech stats: {}\n'.format(pos_counts))


if __name__ == "__main__":
    blog_links = word_client.get(LINKS_KEY)
    if blog_links is None:
        print('Link cache is currently empty. Scraping blog feed at {}'.format(utils.BLOG_FEED_URL))
        blog_links = get_blogpost_links()
    else:
        print('Link cache was hit.')
        blog_links = ast.literal_eval(blog_links.decode('utf-8'))

    if utils.DEBUG_MODE:
        blog_links = [blog_links[0]]

    for link in blog_links:
        parse_blog_post(link)

    get_results()
    error_file.close()
