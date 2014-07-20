from flask import render_template
from . import articles

@articles.route('/')
def articles_index():
  return 'all articles'

@articles.route('/<slug>')
def read_article(slug):
    return 'article: %s' % slug
