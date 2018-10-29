# Lexicount
This is a little tool I wrote to see how obnoxious a writer I am.

# Getting Started
## Setup
The backend for this tool is a simple postgres database. For ease of use, you can set it up using docker:
```bash
cd sqitch/
docker-compose up
```

Also, there's a redis that's used for caching stuff. That's also nice and easy to set up:
```bash
docker pull redis
docker run -d -p 6379:6379 redis
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

## Pre-Commit Hooks
In order to keep my code squeaky clean, this repo features a pre-commit hook that runs autopep8. The formatter needs to be initialized after creating the venv. This can be done by running
```bash
pre-commit install
```
