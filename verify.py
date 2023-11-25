# process cards and comments to ensure we have all the attachments that have been defined.
# this also shows the relationships between attachments and cards/comments
import os
import json


class Config:
    def __init__(self, config_json):
        self.endpoint = config_json['api']
        self.dataPath = config_json['dataDir']
        self.user = config_json['user']
        self.org = config_json['organization']
        self.token = config_json['token']
        self.auth = (self.user, self.token)

def getconfig(filename):
    try:
        with open(filename) as f:
            conf = json.load(f)
    except IOError:
        print('Config file does not exist')
        exit(1)

    new_config: Config = Config(conf)
    return new_config

def loadcards():
    collections = json.load(open('data/selected_collections.json'))

    cards = list()
    for collection in collections:
        collectioncards = collection['cards']
        cards.extend(collectioncards)

    return cards

def getvalidfilename(inputfilename):
    savedFilename = inputfilename
    savedFilename = savedFilename.replace(":", "_")
    savedFilename = savedFilename.replace("\\", "_")
    savedFilename = savedFilename.replace("/", "_")

    return savedFilename

def verifyattachmentsforcards(cards, config):
    for card in cards:
        if not card['attachments']:
            continue

        cardID = card['cardId']
        cardCommonID = card['cardCommonId']
        cardName = card['name']

        for attachment in card['attachments']:
            name = attachment['name']

            cardpath = config.dataPath + "/cards_downloads/" + card['cardId']
            cardpath = cardpath + "/" + card['cardCommonId']

            savedFilename = getvalidfilename(attachment['name'])

            fullpathtofile = cardpath + "/" + savedFilename

            if not os.path.exists(fullpathtofile):
                print(f"failed to locate attached file for card {cardName} {cardID} - {cardCommonID} - {fullpathtofile}")

def getcomments():
    comments = json.load(open('data/selected_comments.json'))
    return comments

def verifyattachmentsforcomments(comments, config):
    for key in comments:
        if not comments[key]:
            continue

        comment = comments[key]
        for commentelement in comment:
            if 'attachments' not in commentelement:
                continue

            for attachment in commentelement['attachments']:
                name = attachment['name']

                commentattachmentpath = config.dataPath + "/comments_downloads/" + commentelement['cardCommonId']
                commentattachmentpath = commentattachmentpath + "/" + commentelement['commentId']

                savedFilename = getvalidfilename(attachment['name'])

                fullpathtofile = commentattachmentpath + "/" + savedFilename
                if not os.path.exists(fullpathtofile):
                    print(f'failed to locate attached file for comment {commentelement["commentId"]} - {commentelement["comment"]} - {fullpathtofile}')


if __name__ == "__main__":
    conf = getconfig('configs/config.json')

    loadedcards = loadcards()
    print(f'loaded {len(loadedcards)} cards')
    verifyattachmentsforcards(loadedcards, conf)

    loadedcomments = getcomments()
    print(f'loaded {len(loadedcomments)} comments')
    verifyattachmentsforcomments(loadedcomments, conf)