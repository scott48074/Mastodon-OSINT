#!/usr/bin/env python3
"""
"""
from bs4 import BeautifulSoup
from collections import Counter
from mastodon import Mastodon
from pathlib import Path
from textblob import TextBlob

API_BASE_URL = 'https://noagendasocial.com'


def register_app():
    # Register app - only once!
    Mastodon.create_app(
        'Mastodon ONSIT',
        to_file='app.secret',
        api_base_url=API_BASE_URL
    )


def login(email, password):
    # Create key for one time log in
    mastodon = Mastodon(client_id='app.secret', api_base_url=API_BASE_URL)
    try:
        mastodon.log_in(
            email,
            password,
            to_file='user.secret',
        )
        return True
    except:
        return False


def create_instance():
    mastodon = Mastodon(
        client_id='app.secret',
        access_token='user.secret',
        api_base_url=API_BASE_URL,
        ratelimit_method='wait'
    )
    return mastodon


def get_toot_sentiment(toot):
        '''
        Utility function to classify sentiment of passed toots
        using textblob's sentiment method
        '''
        # create TextBlob object of passed toot text
        analysis = TextBlob(toot)
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'


def main():
    app_secret = Path('app.secret')
    if not app_secret.is_file():
        register_app()
        print('register')

    user_secret = Path('user.secret')
    if not user_secret.is_file():
        success = False
        while not success:
            email = input('Email: ')
            password = input('Password: ')
            success = login(email, password)

    mastodon = create_instance()
    for key, val in mastodon.account(1).items():
        print(key, val)

    print('#' * 50, '\n')

    sentiment = list()
    for toot in mastodon.account_statuses(1):
        soup = BeautifulSoup(toot['content'], 'html.parser')
        sentiment.append(get_toot_sentiment(soup.get_text()))

    results = Counter(sentiment)
    print(results['negative']/len(sentiment), 'Negative toots')
    print(results['positive']/len(sentiment), 'Positive toots')
    print(results['neutral']/len(sentiment), 'Neutral toots')


if __name__ == '__main__':
    main()
