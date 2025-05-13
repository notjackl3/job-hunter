from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path
from datetime import datetime
from pathlib import Path
from googleapiclient.discovery import build
import pandas as pd

SCOPES = ['https://www.googleapis.com/auth/documents']


def authenticate():
    creds = None
    BASE_DIR = Path(__file__).resolve().parent  # Folder this script is in
    client_secret_path = BASE_DIR / 'client_secret.json'
    token_path = BASE_DIR / 'token.json'

    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                str(client_secret_path), SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    return creds


def create_new_doc(service, creds):
    document = service.documents().create(body={'title': 'New Document'}).execute()
    document_id = document.get('documentId')
    print(f'Document created with ID: {document_id}')


def edit_existing_doc(service, document_id, content):
    doc = service.documents().get(documentId=document_id).execute()
    LAST_INDEX = doc['body']['content'][-1]['endIndex'] - 1
    last_index = LAST_INDEX + 2
    curr_index = last_index
    output_string = ""
    heading_indexes = []
    content_indexes = []
    for key, value in content.items():
        output_string += f"{key.capitalize()}: {value}\n"
        last_index, curr_index = curr_index, curr_index + len(key) + 2  # includes blank space due to newline character
        heading_indexes.append((last_index, curr_index))
        last_index = curr_index
        curr_index += len(str(value)) + 1
        content_indexes.append((last_index, curr_index))

    requests = [
        {
            'insertText': {
                'location': {
                    'index': LAST_INDEX,
                },
                'text': f"\n\n{output_string}"
            }
        },
        {
            "updateTextStyle": {
                "range": {
                    "startIndex": content_indexes[-1][0],
                    "endIndex": content_indexes[-1][1]
                },
                "textStyle": {
                    "link": {
                        "url": content["link"]
                    }
                },
                "fields": "link"
            }
        }
    ]

    for index in heading_indexes:
        requests.append({
            'updateTextStyle': {
                'range': {
                    'startIndex': index[0],
                    'endIndex': index[1]
                },
                'textStyle': {
                    'bold': True,
                },
                'fields': 'bold'
            }})

    result = service.documents().batchUpdate(
        documentId=document_id, body={'requests': requests}).execute()
    print('Text inserted successfully')


def write_doc(csv_file):
    credentials = authenticate()
    service = build('docs', 'v1', credentials=credentials)

    df = pd.read_csv(csv_file)

    for index, row in df.iterrows():
        title = row["title"]
        company = row["company"]
        date_posted = row["date_posted"]
        description = row["description"]
        keywords = ""
        link = row["job_url"]

        content = {"title": title,
                   "company": company,
                   "posted date": date_posted,
                   # "description": self._description, TLDR
                   "keywords": keywords,
                   "link": link}

        edit_existing_doc(service,
                          "18gbVJ2jAmuZbDS1jQ-72SpqpGlWIZmMlNBafId6kTfE",
                          content)


if __name__ == "__main__":
    pass
