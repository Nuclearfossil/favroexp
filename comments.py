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

def load_comments():
    fp = open(dataPath + '\selected_comments.json')
    comments = json.load(fp)
    print(f"Loaded select_comments.json: {len(comments)}")

    return comments

selectedComments = load_comments()

for entry in selectedComments.items():
    for comment in entry[1]:
        if 'attachments' not in comment:
            continue

        for attachment in comment['attachments']:
            print(f"attachment for comment {comment['comment']}")
            print(f"card Common ID {comment['cardCommonId']}")
            print(f"comment ID {comment['commentId']}")
            commentpath = dataPath + "/comments_downloads"
            makedir(commentpath)
            commentpath = commentpath + "/" + comment['cardCommonId']
            makedir(commentpath)
            commentpath = commentpath + "/" + comment['commentId']
            makedir(commentpath)

            print(f"\tattachment name: {attachment['name']}")
            print(f"\tattachment url: {attachment['fileURL']}")

            savedFilename = attachment['name']
            savedFilename = savedFilename.replace(":", "_")
            savedFilename = savedFilename.replace("\\", "_")
            savedFilename = savedFilename.replace("/", "_")
            if os.path.exists(commentpath + "/" + savedFilename):
                continue

            urllib.request.urlretrieve(attachment['fileURL'], commentpath + "/" + savedFilename)
print('Done.')
