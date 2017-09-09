#!/usr/bin/env python
import sys
from multiprocessing import Process
from os import path
from pprint import pprint

import praw
import twitter

import requests
from decouple import config
from jinja2 import Environment, FileSystemLoader
from selenium import webdriver

from separate_process import run_in_separate_process

DEBUG = 0


def get_github():
    """"""
    gh_user = config('github_user')
    github_stars = requests.get('https://api.github.com/users/{}/starred'.format(gh_user)).json()

    github_result = [{'desc': el['description'],
                      'name': el['name'],
                      'url': el['html_url'],
                      'lang': el['language'],
                      'stars': el['stargazers_count'],
                      'update': el['updated_at']} for el in github_stars]
    return github_result, len(github_result)


def get_saved_reddit():
    reddit = praw.Reddit(client_id=config('reddit_client_id'), client_secret=config('reddit_client_secret'),
                         password=config('reddit_password'), user_agent=config('reddit_user_agent'),
                         username=config('reddit_username'))
    # print(reddit)


    me = praw.models.Redditor(reddit, name='tdkte')
    # print(me.saved())
    result = []
    saved = [*me.saved()]
    for x in saved:
        tempd = {}
        try:
            tempd['url'] = x.url,
            tempd['name'] = x.title
            tempd['text'] = x.selftext_html
        except Exception as e:
            tempd['url'] = 'none'
            tempd['name'] = 'comment'
            tempd['text'] = x.body_html
            tempd['obj'] = x
            tempd['errored'] = True
            # pprint(tempd)
            # import ipdb; ipdb.set_trace()
        result.append(tempd)

    return result, len(saved)
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

    likes = api.GetFavorites(count=200)

    return [{'name': f.user.name,
             'url': get_url(f),
             'text': f.text} for f in likes], len(likes)


def show_in_browser(index_path):
    driver = webdriver.Firefox()
    driver.get("file://" + index_path)


def gather_stars(debug=0):

    if debug:
        tweets = get_twitter()
    else:
        reddit_saved, reddit_count = get_saved_reddit()
        tweets, tweet_count = get_twitter()
        gh_stars, gh_count = get_github()
        context = {
            'title': 'Star gatherer by tt',
            'saved': reddit_saved,
            'red_count': reddit_count,
            'tweets': tweets,
            'tweet_count': tweet_count,
            'gh_stars': gh_stars,
            'gh_count': gh_count
        }
        base_dir = path.dirname(path.abspath(__file__))
        rendered = Environment(loader=FileSystemLoader(base_dir)).get_template('index.tmpl').render(context)

        index_path = path.join(base_dir, 'index.html')
        with open(index_path, 'w') as f:
            f.write(rendered)
        return index_path


if __name__ == '__main__':
    show = 1 if len(sys.argv) > 1 else 0
    index_path = gather_stars()
    if show:
        run_in_separate_process(show_in_browser, index_path)
