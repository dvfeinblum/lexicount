import ast
import asyncio
from bs4 import BeautifulSoup
import nltk
import re
import requests as r

from db_utils import update_blog_details, update_word_details, get_unique_words
import utils
from redis_init import LINKS_KEY, word_client

# Some useful constants for parsing blog html
POST_URL_REL = "alternate"
POST_BODY_CLASS = 'post-body entry-content'
blogs_scraped_counter = 0
word_count = 0
pos_counts = {}


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


async def fetch_posts(urls):
    """
    Wrapper that allows blogposts to be fetched asynchronously
    :param urls: List of blog urls
    """
    coroutines = [parse_blog_post(url) for url in urls]
    await asyncio.wait(coroutines)


async def parse_blog_post(blog_link):
    """
    Given a blog post's URL, this function GETs it and pulls the body out.
    We then analyze each word with NTLK and write some data into redis.
    :param blog_link: String
    :return: Raw text from the blog post w/html tags stripped out
    """
    global blogs_scraped_counter
    global word_count
    print('Fetching raw text for {}'.format(blog_link))
    soup = BeautifulSoup(r.get(blog_link).content,
                         features='html.parser')
    post_text = soup.find('div', attrs={'class': POST_BODY_CLASS}).get_text()

    sanitized_post_text = utils.sanitize_blogpost(post_text)
    print('Successfully parsed post. Updating word counts in redis.\n')
    if utils.DEBUG_MODE:
        print('\nSanitized blogpost:\n{clean}\n\nOriginal text:{orig}'.format(clean=sanitized_post_text,
                                                                              orig=post_text))

    [analyze_word(word, blog_link) for word in sanitized_post_text.split(' ')]

    blogs_scraped_counter = blogs_scraped_counter + 1


def analyze_word(word, blog_link):
    """
    Given a word, we figure out its POS and store various info in redis.
    :param word: str
    :param blog_link: url that the word came from, only used for logging
    :return: tuple containing the word and POS of that word
    """
    global word_count
    word_count = word_count + 1

    # Now we do some nltk wizardry
    try:
        pos_array = nltk.pos_tag([word])

        pos_tuple = pos_array[0]
        pos = pos_tuple[1]

        # Send some info to the db
        update_word_details(word, pos)
        update_blog_details(word, blog_link)
        if pos in pos_counts:
            pos_counts[pos] = pos_counts[pos] + 1
        else:
            pos_counts[pos] = 1

        # we don't actually need this but it's useful for testing
        return pos_tuple
    except IndexError:
        # This is the only instance in which an exception is actually cause for concern
        if len(word) > 0:
            print('Failed to nltk-ify a post.\nURL: {url}\nWord: {word}'.format(url=blog_link,
                                                                                word=word))
    except Exception as e:
        print('Word analyzer encountered an unexpected exception on word: {w}\n Exception:{e}'.format(w=word,
                                                                                                      e=e))


def get_results():
    """
    Once the run is complete, we'll spit out some stats.
    """
    # we subtract one because of the blog_links entry
    unique_word_count = get_unique_words()
    print('\nRESULTS\n')
    print('Number of words found across all posts: {}'.format(word_count))
    print('Number of unique words found across all posts: {}'.format(unique_word_count))
    print('Number of posts scraped: {}\n'.format(blogs_scraped_counter))
    print('Average repeat-rate of all words: {}'.format(word_count / unique_word_count))
    print('Average words per post: {}'.format(
        word_count / blogs_scraped_counter))
    print('Unique words per post: {}\n'.format(
        unique_word_count / blogs_scraped_counter))
    print('Part of Speech stats: {}\n'.format(pos_counts))


def main():
    blog_links = word_client.get(LINKS_KEY)
    if blog_links is None:
        print('Link cache is currently empty. Scraping blog feed at {}'.format(
            utils.BLOG_FEED_URL))
        blog_links = get_blogpost_links()
    else:
        print('Link cache was hit.')
        blog_links = ast.literal_eval(blog_links.decode('utf-8'))

    if utils.DEBUG_MODE:
        blog_links = [blog_links[0]]

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(fetch_posts(blog_links))
    finally:
        loop.close()

    get_results()
