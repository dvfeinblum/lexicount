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

# Notes
Right now, this tool is very blunt and there's much I will be changing. Also, sometimes the nltk doesn't quite work because my scraping skills are bad. That's what error.txt is for.
