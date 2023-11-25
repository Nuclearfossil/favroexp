To use:

- install python
- rename sample-config.json to configs\config.json
- fill configs\config.json with real values
- run export with:
	 python export.py
- this will create a data folder, containing
    - collections.json          - the full list of collections in the organization
    - selected_collections.json - the 'selected' collections, as trying to get all the collections in a large org will be very problematic (500 errors)
    - selected_comments.json    - the 'selected' comments
    - widgets.json              - all the widgets in the collections
- to download the file attachments to the cards
    python attachments.py
- this will create, in the data folder, the following directory structure
    - data
        - cards_downloads
            - {cardId}
                - {cardCommonId}
                    - downloaded file(s)
- to download the file attachments for the comments
    python comments.py
- this will create, in the data folder, the followwing directory structure
    - data
        - comments_downloads
            - {cardCommonId}
                - {commentId}
                    - downloaded file(s)