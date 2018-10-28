import psycopg2 as pg

_WORD_DETAILS_TABLE = 'public.word_details'
_BLOG_DETAILS_TABLE = 'public.blog_details'
_PG_USER = 'blog_parser'
_PG_HOST = '0.0.0.0'
_PG_PORT = 5432
_PG_DB = 'lexicount'

_WORD_UPDATE_QUERY = "INSERT INTO " + _WORD_DETAILS_TABLE + \
                     " (word, count, part_of_speech) " \
                     "VALUES ('{word}', 1, '{pos}') " \
                     "ON CONFLICT (word) DO UPDATE SET count = " + \
    _WORD_DETAILS_TABLE + ".count + 1;"
_BLOG_UPDATE_QUERY = "INSERT INTO " + _BLOG_DETAILS_TABLE + \
                     " (word, count, url) " \
                     "VALUES ('{word}', 1, '{url}')" \
                     "ON CONFLICT (word, url) DO UPDATE SET count = " + \
    _BLOG_DETAILS_TABLE + ".count + 1;"
_GET_WORD_COUNT_QUERY = 'SELECT COUNT(DISTINCT word) FROM word_details;'

_db_conn = pg.connect(host=_PG_HOST,
                      port=_PG_PORT,
                      user=_PG_USER,
                      database=_PG_DB)
_db_cursor = _db_conn.cursor()


def execute_query(query):
    """
    Fetches a connection to our pg db
    """
    _db_cursor.execute(query)
    try:
        result = _db_cursor.fetchall()
    except pg.ProgrammingError:
        result = None
    return result


def update_word_details(word, pos):
    """
    Given a word and a part of speech, we update the word_details table
    :param word: it's uh.. a word. Pulled from the blog post being parsed
    :param pos: part of speech as determined by NLTK
    """
    execute_query(_WORD_UPDATE_QUERY.format(word=word,
                                            pos=pos))


def update_blog_details(word, url):
    """
    Given a word and a url, we update the blog_details table
    :param word: yeah again.. it's a word
    :param url: blog's url
    """
    execute_query(_BLOG_UPDATE_QUERY.format(word=word,
                                            url=url))


def get_unique_words():
    """
    Runs a COUNT DISTINCT on the word_details table
    """
    return execute_query(_GET_WORD_COUNT_QUERY)[0][0]


def close_db_connection():
    _db_cursor.close()
    _db_conn.commit()
    _db_conn.close()
