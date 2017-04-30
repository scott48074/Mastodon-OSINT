#!/usr/bin/env python3
"""
"""
from mastodon import Mastodon
from pathlib import Path

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
        api_base_url=API_BASE_URL
    )
    return mastodon


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
    mastodon.toot('Checking to make sure app is only registered once.')


if __name__ == '__main__':
    main()
