from redis import StrictRedis

# Redis stuff
WORD_DB_ID = 0
NLTK_DB_ID = 1
word_client = StrictRedis(db=WORD_DB_ID)
nltk_client = StrictRedis(db=NLTK_DB_ID)
LINKS_KEY = 'blog_links'
