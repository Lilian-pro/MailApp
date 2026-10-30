Authentification & autorisation
Token d'accès pour les APIs concernés, NE PAS PARTAGEZ CE TOKEN.


créer un venv et dedans installer :
python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib beautifulsoup4


Lancer le quickstart pour générer un Token. Si c'est la première fois vous serez redirigez sur une page web pour vous authentifier et créer le credentials nécessaire.

SCOPES = ["https://mail.google.com/"]

Le SCOPES définit quel genre d'autorisation vous donnez à votre service. Ici tous les droits.


librairies utilisées :

import base64

import os

from bs4 import BeautifulSoup

from googleapiclient.discovery import build

from google.auth.transport.requests import Request

from google.oauth2.credentials import Credentials

from google_auth_oauthlib.flow import InstalledAppFlow

from googleapiclient.errors import HttpError


Situation de l'API de l'application:

callGMail.py :

getCreds() #The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.

getMessageById(message_id) #Récupère un message par son ID.

getMessagePayload(message_id) #Récupère et décode le texte d'un message Gmail.

findBodyByMimeType(payload, mime_type) #Recherche et décode récursivement une partie MIME précise.

decode_message_body(payload) #Décode le texte d'un payload Gmail, y compris les messages multipart.

getLabelsIdByName(label_name) #Récupère l'ID d'un label Gmail par son nom.

setLabels(message_id, label_ids) #Ajoute des labels à un message Gmail.

parseHtml.py :

parse_html_message(html) #Conserve le texte et les URLs d'un message HTML.


TODO: 
  Mettre en fonction TFIDFmail pour faciliter la lecture dans le main.
  Faire les premiers appellent à callGMail pour trier les mails dans le gmail pro.
  Faire en sorte d'ajouter au fichier json les nouveaux mails BIEN labellisés.
