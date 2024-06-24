import os.path
import google.auth
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

SCOPES = 'https://www.googleapis.com/auth/drive'


def upload_basic():
  
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  os.chdir(r'C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main')
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      os.chdir(r'C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main')
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

  try:
    # create drive api client
    service = build("drive", "v3", credentials=creds)

    results = service.drives().list(pageSize=10).execute()
    shared_drive_id = results['drives'][2]['id']
    folders_names = service.files().list(pageSize=10).execute()
    os.chdir(r'C:/Users/Irvin/Coding Projects/FarmBot-API-scripts-main/Images')
    file_metadata = { 
        "name": "0w1k5ne2vdaxoebj9iw3nh06u2u3.jpg",
        "mimeType": 'image/jpeg',
        "parents": [shared_drive_id]}
    media = MediaFileUpload("0w1k5ne2vdaxoebj9iw3nh06u2u3.jpg", mimetype="image/jpeg")
    # pylint: disable=maybe-no-member
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, supportsAllDrives=True,)
        .execute()
    )
    print(f'File ID: {file.get("id")}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    file = None

  return file.get("id")


if __name__ == "__main__":
  upload_basic()