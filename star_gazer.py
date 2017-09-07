#!/usr/bin/env python
import praw
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver
import os
from decouple import config
import twitter

DEBUG = 0


def get_saved_reddit():
    reddit = praw.Reddit(client_id=config('reddit_client_id'), client_secret=config('reddit_client_secret'),
                         password=config('reddit_password'), user_agent=config('reddit_user_agent'),
                         username=config('reddit_username'))
    # print(reddit)

    me = praw.models.Redditor(reddit, name='tdkte')
    # print(me.saved())
    result = []
    for x in me.saved():
        try:
            tempd = {
                 'url': x.url,
                }
            tempd['name'] = x.title
            tempd['text'] = x.selftext_html
        except Exception as e:
            print('catched')
            print(dir(x))
            print(x.body)
            tempd['url'] = 'none'
            tempd['name'] = 'comment'
            tempd['text'] = x.body_html
            tempd['obj'] = x
            print(e)
        result.append(tempd)
    return result
    # https://pl.reddit.com/user/tdkte/saved/




def get_twitter():
    api = twitter.Api(consumer_key=config('twitter_consumer_key'),
                      consumer_secret=config('twitter_consumer_secret'),
                      access_token_key=config('twitter_access_token_key'),
                      access_token_secret=config('twitter_access_token_secret'))

    def get_url(f):
        try:
            url = f.urls[0].url
        except:
            url = '#'
        finally:
            return url

    return [{'name': f.user.name,
             'url': get_url(f),
             'text': f.text} for f in api.GetFavorites(count=200)]


def gather_stars(show=0, debug=0):

    if debug:
        tweets = get_twitter()
    else:
        context = {
            'title': 'Star gatherer by tt',
            'saved': get_saved_reddit(),
            'tweets': get_twitter()
        }
        path = None
        rendered = Environment(loader=FileSystemLoader(path or './')
                ).get_template('index.tmpl').render(context)
        # rendered_old = Environment().from_string(HTML).render(title='Hellow Gist from GutHub',
            # saved=saved, tweets=tweets)
        with open('index.html', 'w') as f:
            f.write(rendered)
        uri = os.path.join(os.getcwd(), 'index.html')
        if show:
            driver = webdriver.Firefox()
            driver.get("file://" + uri)


if __name__ == '__main__':
    gather_stars(show=0)
