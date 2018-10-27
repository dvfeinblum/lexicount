import psycopg2 as pg

_WORD_DETAILS_TABLE = 'public.word_details'
_BLOG_DETAILS_TABLE = 'public.blog_details'
_PG_USER = 'blog_parser'
_PG_HOST = '0.0.0.0'
_PG_PORT = 5432
_PG_DB = 'lexicount'

_WORD_UPDATE_QUERY = ''
_BLOG_UPDATE_QUERY = ''
_GET_WORD_COUNT_QUERY = 'SELECT COUNT(DISTINCT word) FROM word_details;'

_db_conn = pg.connect(host=_PG_HOST,
                      port=_PG_PORT,
                      user=_PG_USER,
                      database=_PG_DB)


def get_cursor():
    """
    Fetches a connection to our pg db
    """
    return _db_conn.cursor()


def update_word_details(word, pos):
    """
    Given a word and a part of speech, we update the word_details table
    :param word: it's uh.. a word. Pulled from the blog post being parsed
    :param pos: part of speech as determined by NLTK
    """
    return


def update_blog_details(word, url):
    """
    Given a word and a url, we update the blog_details table
    :param word: yeah again.. it's a word
    :param url: blog's url
    """
    return


def get_unique_words():
    """
    Runs a COUNT DISTINCT on the word_details table
    """
    cursor = get_cursor()
    return cursor.execute(_GET_WORD_COUNT_QUERY)
