# Download the attachments for cards.
import os
import json
import urllib.request

try:
    with open('configs/config.json') as f:
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


def makedir(dataPath):
    if not os.path.exists(dataPath):
        try:
            os.mkdir(dataPath)
        except:
            print('Data directory could not be created')
            exit(1)


def load_collections():
    fp = open(dataPath + '\selected_collections.json')
    collections = json.load(fp)
    print(f"Loaded select_collections.json: {len(collections)}")

    return collections


selectedCollections = load_collections()

for collection in selectedCollections:
    cards = collection['cards']
    if len(cards) == 0:
        print("No cards found")
        exit(-1)
    for card in cards:
        if len(card['attachments']) == 0:
            continue

        attachments = card['attachments']

        print(f"attachment for card {card['name']}")
        print(f"card ID {card['cardId']}")
        print(f"card Common ID {card['cardCommonId']}")
        cardpath = dataPath + "/cards_downloads/" + card['cardId']
        makedir(cardpath)
        cardpath = cardpath + "/" + card['cardCommonId']
        makedir(cardpath)
        for attachment in attachments:
            print(f"\tattachment name: {attachment['name']}")
            print(f"\tattachment url: {attachment['fileURL']}")
            if os.path.exists(cardpath + "/" + attachment['name']):
                print(f"\tskipping {attachment['name']}")
                continue

            savedFilename = attachment['name']
            savedFilename = savedFilename.replace(":", "_")
            savedFilename = savedFilename.replace("\\", "_")
            savedFilename = savedFilename.replace("/", "_")
            urllib.request.urlretrieve(attachment['fileURL'], cardpath + "/" + savedFilename)

print('Done.')
