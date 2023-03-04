from __future__ import print_function

import auth
from client import ApiClient
import util

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
# Number of emails retrieved
MAIL_COUNTS = 5
# Search criteria
SEARCH_CRITERIA = {
    'from': "no-reply@mail.instagram.com",
    'to': "",
    'subject': ""
}
BASE_DIR = 'mail_box'


def build_search_criteria(query_dict):
    query_string = ''
    for key, value in query_dict.items():
        if value:
            query_string += key + ':' + value + ' '

    return query_string


def main():
    creds = auth.authenticate(SCOPES)

    query = build_search_criteria(SEARCH_CRITERIA)

    client = ApiClient(creds)
    messages = client.get_mail_list(MAIL_COUNTS, query)

    if not messages:
        print('No message list.')
    else:
        
        message_id = messages[0]['id']

        # get subject and message
        result = client.get_subject_message(message_id)
        print(result[0][:6])
        # save file
        # util.save_file(BASE_DIR, result)


if __name__ == '__main__':
    main()
