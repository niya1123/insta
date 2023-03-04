from google.oauth2.credentials import Credentials
import google_auth_oauthlib
from googleapiclient.discovery import build

# OAuth 2.0クライアントIDを取得する
client_config = {'installed': {'client_id': '663205835356-mf9vfjh7qvgucrp05ck3or8mjps7hr4b.apps.googleusercontent.com',
                               'client_secret': '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',
                               'redirect_uris': ['urn:ietf:wg:oauth:2.0:oob', 'http://localhost']}}

# OAuth 2.0の認証フローを開始する
appflow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_config(client_config, ['https://www.googleapis.com/auth/gmail.readonly'])
creds = appflow.run_local_server(port=0)

# 認証情報をローカルファイルに保存する
with open('token.json', 'w') as token:
    token.write(creds.to_json())

# Gmail APIを使って新着メールを取得する
service = build('gmail', 'v1', credentials=creds)
result = service.users().messages().list(maxResults=5, userId='me', q='is:unread').execute()
messages = result.get('messages')

if not messages:
    print('No new messages.')
else:
    print('New messages:')
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        payload = msg['payload']
        headers = payload['headers']
        for header in headers:
            if header['name'] == 'From':
                print('From:', header['value'])
            if header['name'] == 'Subject':
                print('Subject:', header['value'])
        snippet = msg['snippet']
        print('Snippet:', snippet)
