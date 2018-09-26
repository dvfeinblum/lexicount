# Lexicount
This is a little tool I wrote to see how obnoxious a writer I am.

# Getting Started
## Setup
You'll need to do a few things if you want to run this tool. First off, you need docker. Once you have it up and running:
```
docker pull redis
```
as we'll be using it to store results. Next, you need to get the cache up and running with:
```
docker run -d -p 6379:6379 redis
```

Now that you have the cache, you're actually ready to go. Set up a `venv` and install requirements with:
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
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
