import os
import json
import time
import requests
import urllib
import dateutil.parser
# import pytz
from datetime import datetime
from datetime import timezone

try:
    with open('configs\\config.json') as f:
        conf = json.load(f)
except IOError:
    print('Config file does not exist')
    exit(1)

url = conf['api']
dataPath = conf['dataDir']
user = conf['user']
org = conf['organization']
token = conf['token']
auth = (user, token)


def rate_limit_exceeded_and_sleep(response):
    if response.status_code != 429:
        return False

    date_str = response.headers['X-RateLimit-Reset']
    reset_date = dateutil.parser.parse(date_str)
    now = datetime.now(timezone.utc)

    span = reset_date - now

    print('Request limit for Favro\'s API has exceeded and will reset at {0}'.format(reset_date))
    print('[{0}] Waiting {1} minutes for reset...'.format(datetime.now(), int(span.seconds // 60.0)))
    time.sleep(span.seconds + 1)

    print('Continue...')

    return True


def get_url(method):
    return url + method


def get_collections(archived=False):
    path = get_url("collections")
    headers = {
        "organizationId": org
    }

    params = {}
    if archived:
        params['archived'] = "true"

    r = requests.get(path, headers=headers, params=params, auth=auth)
    if rate_limit_exceeded_and_sleep(r):
        r = requests.get(path, headers=headers, params=params, auth=auth)

    if r.status_code != 200:
        print('Error getting collections: ', r.status_code)
        print(r.json())
        exit(1)

    server = r.headers['X-Favro-Backend-Identifier']
    data = r.json()
    entities = data['entities']
    page = data['page']
    pages = data['pages']
    request_id = data['requestId']
    headers['X-Favro-Backend-Identifier'] = server
    params['requestId'] = request_id

    for page in range(1, pages):
        params['page'] = page
        r = requests.get(path, headers=headers, params=params, auth=auth)
        if rate_limit_exceeded_and_sleep(r):
            r = requests.get(path, headers=headers, params=params, auth=auth)
        if r.status_code != 200:
            print('Error getting subsequent collections: ', r.status_code)
            print(r.json())
            exit(1)
        entities.extend(r.json()['entities'])
    return entities


def get_select_collections():
    entities = [
        {
            "name": "Relish",
            "collectionId": "0553ed1151256cc2c6bcb998"
        },
        {
            "name": "Core - Meta",
            "collectionId": "e7cfa959c7ee456a2700f28d"
        },
        {
            "name": "Meta Project Status",
            "collectionId": "7d68353be445fc2630fc1f1c"
        },
        {
            "name": "Brisbane",
            "collectionId": "92a21306751cb128050d951f"
        }
    ]
    return entities


def get_widgets(archived=False):
    path = get_url('widgets')
    headers = {
        "organizationid": org
    }
    params = {}
    if archived:
        params['archived'] = "true"

    r = requests.get(path, headers=headers, params=params, auth=auth)
    if rate_limit_exceeded_and_sleep(r):
        r = requests.get(path, headers=headers, params=params, auth=auth)
    if r.status_code != 200:
        print('Error getting widgets: ', r.status_code)
        print(r.json())
        exit(1)

    server = r.headers['X-Favro-Backend-Identifier']
    data = r.json()
    entities = data['entities']
    page = data['page']
    pages = data['pages']
    request_id = data['requestId']
    headers['X-Favro-Backend-Identifier'] = server
    params['requestId'] = request_id

    for page in range(1, pages):
        params['page'] = page
        r = requests.get(path, headers=headers, params=params, auth=auth)
        if rate_limit_exceeded_and_sleep(r):
            r = requests.get(path, headers=headers, params=params, auth=auth)
        if r.status_code != 200:
            print('Error getting subsequent widgets: ', r.status_code)
            print(r.json())
            exit(1)
        entities.extend(r.json()['entities'])

    return entities


def get_cards_for_collection(collectionId, archived=False):
    path = get_url('cards')
    headers = {
        "organizationid": org
    }
    params = {
        "collectionId": collectionId
    }
    if archived:
        params['archived'] = "true"

    r = requests.get(path, headers=headers, params=params, auth=auth)
    if rate_limit_exceeded_and_sleep(r):
        r = requests.get(path, headers=headers, params=params, auth=auth)
    if r.status_code != 200:
        print('Error getting cards: ', r.status_code)
        print(r.json())
        exit(1)

    server = r.headers['X-Favro-Backend-Identifier']
    data = r.json()
    entities = data['entities']
    page = data['page']
    pages = data['pages']
    request_id = data['requestId']
    headers['X-Favro-Backend-Identifier'] = server
    params['requestId'] = request_id

    for page in range(1, pages):
        params['page'] = page
        r = requests.get(path, headers=headers, params=params, auth=auth)
        if rate_limit_exceeded_and_sleep(r):
            r = requests.get(path, headers=headers, params=params, auth=auth)
        if r.status_code != 200:
            print('Error getting subsequent cards: ', r.status_code)
            print(r.json())
            exit(1)
        entities.extend(r.json()['entities'])

    return entities


def get_cards_for_widget(widgetId, archived=False):
    path = get_url('cards')
    headers = {
        "organizationid": org
    }
    params = {
        "widgetCommonId": widgetId
    }
    if archived:
        params['archived'] = "true"

    r = requests.get(path, headers=headers, params=params, auth=auth)
    if rate_limit_exceeded_and_sleep(r):
        r = requests.get(path, headers=headers, params=params, auth=auth)
    if r.status_code != 200:
        print('Error getting cards: ', r.status_code)
        print(r.json())
        exit(1)

    server = r.headers['X-Favro-Backend-Identifier']
    data = r.json()
    entities = data['entities']
    page = data['page']
    pages = data['pages']
    request_id = data['requestId']
    headers['X-Favro-Backend-Identifier'] = server
    params['requestId'] = request_id

    for page in range(1, pages):
        params['page'] = page
        r = requests.get(path, headers=headers, params=params, auth=auth)
        if rate_limit_exceeded_and_sleep(r):
            r = requests.get(path, headers=headers, params=params, auth=auth)
        if r.status_code != 200:
            print('Error getting subsequent cards: ', r.status_code)
            print(r.json())
            exit(1)
        entities.extend(r.json()['entities'])

    return entities


def get_columns(widgetId):
    path = get_url('columns')
    headers = {
        "organizationid": org
    }
    params = {
        "widgetCommonId": widgetId
    }

    r = requests.get(path, headers=headers, params=params, auth=auth)
    if rate_limit_exceeded_and_sleep(r):
        r = requests.get(path, headers=headers, params=params, auth=auth)
    if r.status_code != 200:
        print('Error getting columns: ', r.status_code)
        print(r.json())
        exit(1)

    server = r.headers['X-Favro-Backend-Identifier']
    data = r.json()
    entities = data['entities']
    page = data['page']
    pages = data['pages']
    request_id = data['requestId']
    headers['X-Favro-Backend-Identifier'] = server
    params['requestId'] = request_id

    for page in range(1, pages):
        params['page'] = page
        r = requests.get(path, headers=headers, params=params, auth=auth)
        if rate_limit_exceeded_and_sleep(r):
            r = requests.get(path, headers=headers, params=params, auth=auth)
        if r.status_code != 200:
            print('Error getting subsequent columns: ', r.status_code)
            print(r.json())
            exit(1)
        entities.extend(r.json()['entities'])

    return entities


def get_tags():
    path = get_url('tags')
    headers = {
        "organizationid": org
    }

    params = {}

    r = requests.get(path, headers=headers, params=params, auth=auth)
    if rate_limit_exceeded_and_sleep(r):
        r = requests.get(path, headers=headers, params=params, auth=auth)
    if r.status_code != 200:
        print('Error getting tags: ', r.status_code)
        print(r.json())
        exit(1)

    server = r.headers['X-Favro-Backend-Identifier']
    data = r.json()
    entities = data['entities']
    page = data['page']
    pages = data['pages']
    request_id = data['requestId']
    headers['X-Favro-Backend-Identifier'] = server
    params['requestId'] = request_id

    for page in range(1, pages):
        params['page'] = page
        r = requests.get(path, headers=headers, params=params, auth=auth)
        if rate_limit_exceeded_and_sleep(r):
            r = requests.get(path, headers=headers, params=params, auth=auth)
        if r.status_code != 200:
            print('Error getting subsequent tags: ', r.status_code)
            print(r.json())
            exit(1)
        entities.extend(r.json()['entities'])

    return entities


def get_comments(cardId):
    path = get_url('comments')
    headers = {
        "organizationid": org
    }

    params = {
        "cardCommonId": cardId
    }

    r = requests.get(path, headers=headers, params=params, auth=auth)
    if rate_limit_exceeded_and_sleep(r):
        r = requests.get(path, headers=headers, params=params, auth=auth)
    if r.status_code != 200:
        print('Error getting comments: ', r.status_code)
        print(r.json())
        exit(1)

    server = r.headers['X-Favro-Backend-Identifier']
    data = r.json()
    entities = data['entities']
    page = data['page']
    pages = data['pages']
    request_id = data['requestId']
    headers['X-Favro-Backend-Identifier'] = server
    params['requestId'] = request_id

    for page in range(1, pages):
        params['page'] = page
        r = requests.get(path, headers=headers, params=params, auth=auth)
        if rate_limit_exceeded_and_sleep(r):
            r = requests.get(path, headers=headers, params=params, auth=auth)
        if r.status_code != 200:
            print('Error getting subsequent comments: ', r.status_code)
            print(r.json())
            exit(1)
        entities.extend(r.json()['entities'])

    return entities

if __name__ == "__main__":
    # --------------------------------------
    # Initialize
    # --------------------------------------
    if not os.path.exists(dataPath):
        try:
            os.mkdir(dataPath)
        except:
            print('Data directory could not be created')
            exit(1)

    # --------------------------------------
    # Download
    # --------------------------------------

    print('Downloading collections...')
    # if you're geting the full list of collections, uncomment out the content below
    # collections = get_collections()
    # collections.extend(get_collections(archived=False))

    # collections_path = os.path.join(dataPath, 'collections.json')
    # with open(collections_path, "w") as f:
    #  json.dump(collections, f, indent=1, sort_keys=False)

    # otherwise, use the following
    collections = get_select_collections()
    collectionnames = [collection['name'] for collection in collections]

    print('Found ', len(collections))

    print('Downloading tags...')
    tags = get_tags()
    print('Found ', len(tags))

    tags_path = os.path.join(dataPath, 'tags.json')
    with open(tags_path, "w") as f:
        json.dump(tags, f, indent=1, sort_keys=False)


    print('Downloading widgets...')
    widgets = get_widgets()
    widgets.extend(get_widgets(archived=False))
    print('Found ', len(widgets))

    card_common_ids = set()

    print('Downloading cards...')
    for collection in collections:
        print('Downloading cards for collection: ', collection.get('name'))
        cards = list()
        cards.extend(get_cards_for_collection(collection.get('collectionId')))
        cards.extend(get_cards_for_collection(collection.get('collectionId'), archived=False))
        collection['cards'] = cards
        print('Found ', len(cards))
        for card in cards:
            card_common_ids.add(card['cardCommonId'])

    for widget in widgets:
        if widget.get('name') not in collectionnames:
            continue
        print('Downloading cards for widget: ', widget.get('name'))
        cards = list()
        cards.extend(get_cards_for_widget(widget.get('widgetCommonId')))
        cards.extend(get_cards_for_widget(widget.get('widgetCommonId'), archived=False))
        widget['cards'] = cards
        print('Found ', len(cards))
        for card in cards:
            card_common_ids.add(card['cardCommonId'])

    print('Downloading columns...')
    for widget in widgets:
        if widget.get('name') not in collectionnames:
            continue
        print('Downloading columns for widget: ', widget.get('name'))
        widget['columns'] = get_columns(widget.get('widgetCommonId'))
        print('Found', len(widget['columns']))

    comments = dict()
    print('Downloading comments. This could take a while...')
    cardindex = 1
    for card_common_id in card_common_ids:
        print(f'Downloading card index {cardindex}/{len(card_common_ids)}')
        comments[card_common_id] = get_comments(card_common_id)

    comment_count = sum(len(v) for k, v in comments.items())
    print('Found ', comment_count)

    # --------------------------------------
    # Store
    # --------------------------------------
    collections_path = os.path.join(dataPath, 'select_collections.json')
    with open(collections_path, "w") as f:
        json.dump(collections, f, indent=1, sort_keys=False)

    widgets_path = os.path.join(dataPath, 'widgets.json')
    with open(widgets_path, "w") as f:
        json.dump(widgets, f, indent=1, sort_keys=False)

    comments_path = os.path.join(dataPath, 'selected_comments.json')
    with open(comments_path, "w") as f:
        json.dump(comments, f, indent=1, sort_keys=False)

    print('Done.')
