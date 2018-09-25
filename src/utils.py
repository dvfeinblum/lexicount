import string

# To remove punctuation, we use a translator
translator = str.maketrans('', '', string.punctuation)


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
