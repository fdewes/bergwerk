import os
import sys
import requests
from time import sleep

API_URL = 'http://bergwerk-wiki/w/api.php'
USERNAME = os.getenv('BOT_USERNAME')
PASSWORD = os.getenv('BOT_PASSWORD')


def login():
    session = requests.Session()

    # Get login token
    response = session.get(API_URL, params={
        'action': 'query',
        'meta': 'tokens',
        'type': 'login',
        'format': 'json'
    })
    login_token = response.json()['query']['tokens']['logintoken']

    # Log in
    response = session.post(API_URL, data={
        'action': 'login',
        'lgname': USERNAME,
        'lgpassword': PASSWORD,
        'lgtoken': login_token,
        'format': 'json'
    })

    print(response.json())

    if response.json()['login']['result'] != 'Success':
        raise Exception('Failed to log in')

    return session


def get_csrf_token(session):
    response = session.get(API_URL, params={
        'action': 'query',
        'meta': 'tokens',
        'format': 'json'
    })
    return response.json()['query']['tokens']['csrftoken']


def create_or_update_page(session, csrf_token, title, content):

    response = session.post(API_URL, data={
        'action': 'edit',
        'title': title,
        'text': content,
        'token': csrf_token,
        'format': 'json'
    })
    if 'error' in response.json():
        raise Exception(response.json()['error'])
    return response.json()


def main():

    connected = False

    while not connected:
        try:
            session = login()
            connected = True
        except:
            print("Error logging in. retrying in 5 secs...")
            sleep(5)
    csrf_token = get_csrf_token(session)

    for filename in os.listdir('/tmp/data'):
        if filename.endswith('.wikitext'):
            # Remove '.wikitext' extension to get the title
            title = filename[:-9].replace("_", " ")
            with open(os.path.join('/tmp/data', filename), 'r') as file:
                content = file.read()
            print(f'Creating page: {title}')
            response = create_or_update_page(
                session, csrf_token, title, content)
            sys.stdout.flush()


if __name__ == '__main__':
    main()
