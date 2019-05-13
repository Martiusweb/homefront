# coding: utf-8
import datetime
import os

AUTHOR = 'Martin Richard'
SITENAME = 'Martin Richard'
SITESUBTITLE = "Hello, I'm Martin, and this is my webpage."
SITEURL = ''

MENUITEMS = (
    # Put this page first (it's "hidden" and must appear before categories in
    # the menu)
    ("About me", "aboutme.html"),
)

PATH = 'content'
STATIC_PATHS = ("images",)

# We want "pages" to be in the root directory
PAGE_URL = "{slug}.html"
PAGE_SAVE_AS = "{slug}.html"

# Customize the scheme of urls for articles to match existing articles
INDEX_SAVE_AS = 'w/index.html'
ARTICLE_URL = 'w/{date:%Y}-{date:%m}-{date:%d}-{slug}.html'
ARTICLE_SAVE_AS = 'w/{date:%Y}-{date:%m}-{date:%d}-{slug}.html'

ARTICLE_LANG_URL = 'w/{date:%Y}-{date:%m}-{date:%d}-{slug}-{lang}.html'
ARTICLE_LANG_SAVE_AS = 'w/{date:%Y}-{date:%m}-{date:%d}-{slug}-{lang}.html'

DEFAULT_CATEGORY = "hidden"
CATEGORY_URL = "{slug}/"
CATEGORY_SAVE_AS = "{slug}/index.html"
# This allows us to write /(t|w)/index.html
TAG_URL = "{slug}/"
TAG_SAVE_AS = "{slug}/index.html"

# Because of talks
USE_FOLDER_AS_CATEGORY = False

TIMEZONE = 'Europe/Paris'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = "theme/default"

NOW = datetime.datetime.now()
DATE_FORMATS = {
    'fr': '%d %b %Y',
    'en': '%d %b %Y',
}
