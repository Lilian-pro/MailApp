import base64
import os

from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


SCOPES = ["https://mail.google.com/"]

def getCreds():
  """Crée le token et les credentials nécessaires"""
  creds = None
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json")
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
  
  return creds

service = build('gmail', 'v1', credentials=getCreds())


def getMessageById(message_id):
    """Récupère un message par son ID."""
    try:
        message = service.users().messages().get(userId='me', id=message_id).execute()
        return message
    except Exception as e:
        print(f"Erreur lors de la récupération du message : {e}")
        return None

def getMessagePayload(message_id):
    """Récupère et décode le texte d'un message Gmail."""
    message = getMessageById(message_id)
    if not message:
        return {}
    return message.get("payload", {})

def findBodyByMimeType(payload, mime_type):
    """Recherche et décode récursivement une partie MIME précise."""
    if payload.get("mimeType") == mime_type:
        body_data = payload.get("body", {}).get("data")
        if body_data:
            decoded = base64.urlsafe_b64decode(
                body_data + "=" * (-len(body_data) % 4)
            )
            return decoded.decode("utf-8", errors="replace")

    for part in payload.get("parts", []):
        decoded = findBodyByMimeType(part, mime_type)
        if decoded:
            return decoded

    return ""

def decode_message_body(payload):
    """Décode le texte brut, puis le HTML si le texte brut est absent."""
    plain_text = findBodyByMimeType(payload, "text/plain")
    if plain_text != "undefined\r\n" and plain_text != "":
        return plain_text

    return findBodyByMimeType(payload, "text/html")


def getLabelsIdByName(label_name):
    """Récupère l'ID d'un label Gmail par son nom."""
    try:
        labels = service.users().labels().list(userId='me').execute().get('labels', [])
        for label in labels:
            if label['name'] == label_name:
                return label['id']
        print(f"Label '{label_name}' non trouvé.")
        return None
    except Exception as e:
        print(f"Erreur lors de la récupération des labels : {e}")
        return None

def setLabels(message_id, label_ids):
    """Ajoute des labels à un message Gmail."""
    try:
        service.users().messages().modify(
            userId='me',
            id=message_id,
            body={'addLabelIds': label_ids}
        ).execute()
        print(f"Labels {label_ids} ajoutés au message {message_id}.")
    except Exception as e:
        print(f"Erreur lors de l'ajout des labels : {e}")
