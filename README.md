Authentification & autorisation
Token d'accès pour les APIs concernés, NE PAS PARTAGEZ CE TOKEN.


Avant même de faire quoi que ce soit il vous faudra un fichier credentials.json que vous obtenez sur la console google cloud, assurez-vous d'avoir bien activé l'API Gmail (allez dans API et services > Bibliothèque, cherchez Gmail API et cliquez sur Activer). Allez dans API et services > Identifiants (Credentials). Cliquez sur Créer des identifiants en haut, puis sélectionnez ID client OAuth. Si on vous demande de configurer l'écran de consentement OAuth au préalable :

* Choisissez Externe (sauf si vous êtes sur un compte Google Workspace d'entreprise/école).

* Remplissez le nom de l'app et votre e-mail, puis enregistrez (vous pouvez passer les étapes facultatives).

Revenez à la création de l'ID client :

* Type d'application : Application de bureau (Desktop app).

* Donnez-lui un nom (ex: Gmail Quickstart) et cliquez sur Créer.

Dans la liste de vos identifiants OAuth, repérez celui que vous venez de créer.

Cliquez sur l'icône de téléchargement (la petite flèche vers le bas) située à droite de la ligne. Cela va télécharger un fichier JSON (souvent nommé avec une suite de chiffres et lettres).

Renommez ce fichier téléchargé exactement en : credentials.json.
Déplacez ce fichier dans le même dossier où se trouve votre script quickstart.py


Il faudra renseigner l'adresse mail avec laquelle vous voulez utilisez l'application dans Google Auth Platform/Audience, vous ajoutez un utilisateur test.


créer un venv et dedans installer :
python3 -m pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib beautifulsoup4


Lancer le quickstart pour générer un Token. Si c'est la première fois vous serez redirigez sur une page web pour vous authentifier et créer le token.

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
  Faire les premiers appellent à callGMail pour trier les mails dans le gmail pro.
  Faire en sorte d'ajouter au fichier json les nouveaux mails BIEN labellisés.

