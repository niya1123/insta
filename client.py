
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import util


class ApiClient(object):

    def __init__(self, credential):
        self.service = build('gmail', 'v1', credentials=credential)

    def get_mail_list(self, limit, query):
        # Call the Gmail API
        try:
            results = self.service.users().messages().list(
                userId='me', maxResults=limit, q=query).execute()
        except HttpError as err:
            print(f'action=get_mail_list error={err}')
            raise

        messages = results.get('messages', [])

        return messages

    def get_subject_message(self, id):
        # Call the Gmail API
        try:
            res = self.service.users().messages().get(userId='me', id=id).execute()
        except HttpError as err:
            print(f'action=get_message error={err}')
            raise

        # result = {}

        subject = [d.get('value') for d in res['payload']['headers'] if d.get('name') == 'Subject']
        # result['subject'] = subject

        # # Such as text/plain
        # if 'data' in res['payload']['body']:
        #     b64_message = res['payload']['body']['data']
        # # Such as text/html
        # elif res['payload']['parts'] is not None:
        #     b64_message = res['payload']['parts'][0]['body']['data']
        # message = util.base64_decode(b64_message)
        # result['message'] = message

        return subject