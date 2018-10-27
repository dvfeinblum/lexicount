import psycopg2 as pg

_WORD_DETAILS_TABLE = 'public.word_details'
_BLOG_DETAILS_TABLE = 'public.blog_details'
_PG_USER = 'blog_parser'
_PG_HOST = '0.0.0.0'
_PG_PORT = 5432
_PG_DB = 'lexicount'


def get_connection():
    return pg.connect(host=_PG_HOST,
                      port=_PG_PORT,
                      user=_PG_USER,
                      database=_PG_DB)


def update_word_details(word, pos):
    return


def update_blog_details(word, url):
    return


def get_unique_words():
    return
