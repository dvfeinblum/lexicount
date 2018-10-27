# Lexicount
This is a little tool I wrote to see how obnoxious a writer I am.

# Getting Started
## Setup
The backend for this tool is a simple postgres database. For ease of use, you can set it up using docker:
```
cd sqitch/
docker-compose up
```

Now that you have the db, you're actually ready to go. Set up a `venv` and install requirements with:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

NOTE: NLTK requires various downloads to work properly. Once you've finished installing the requirements, you should open a python REPL and run the following:
```
>>> import nltk
>>> nltk.download('averaged_perceptron_tagger')
```

## Running the thing
Once you get that working, you're basically all set. Simply run:
```
python src/run.py
```
and it should get going on its own.

Oh! Also. If you would like to crawl along your own blog, there are a couple things you have to do:

1. Make sure you have a blogpost.com blog. Currently, there's some hardcoded stuff that assumes you'll be using a feed from one of those.
1. Set this envvar:
```bash
BLOG_FEED_URL="http://[YOUR USER NAME].blogspot.com/feeds/posts/default"
```

and that's it! The script will do the rest.

# Notes
Right now, this tool is very blunt and there's much I will be changing. Also, sometimes the nltk doesn't quite work because my scraping skills are bad. That's what error.txt is for.

Oh and another thing, feel free to click over to the issues to see what I have planned next!
