from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import json

with open("dataset_mails_100.json", "r") as f:
    data = json.load(f)

type_retour = ["acceptation", "entretien", "refus", "confirmation candidature"]

# 1. Exemples d'entraînement (Texte -> Catégorie)
mails = []
labels = []
for item in data: 
    mails.append(item["corpus"])
    labels.append(item["label"])

# 2. Transformation et entraînement de l'algorithme
vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(mails)

model = LogisticRegression()
model.fit(X, labels)



# 3. Tests

#acceptation = ["Bonjour [Prénom du candidat], Un grand merci pour le temps accordé tout au long de notre processus de recrutement. Toute l’équipe a été ravie de faire votre connaissance et nous avons été particulièrement impressionnés par vos compétences ainsi que votre dynamisme. C'est donc avec grand plaisir que nous vous proposons officiellement le poste de [Intitulé du poste] au sein de [Nom de l'entreprise] !"]
#entretien = ["Bonjour [Prénom du candidat], Votre candidature pour le poste de [Intitulé du poste] a retenu toute notre attention. Vos compétences et votre parcours correspondent tout à fait au profil que nous recherchons. Afin de faire plus ample connaissance et d'échanger sur vos motivations, nous serions ravis de vous inviter à un entretien d'embauche."]
#refus = ["Nous avons étudié votre dossier de candidature pour l'offre Alternance - Bac+2/+3 - Développement d'un progiciel python pour le pilotage d'un accélérateur - H/F référence 2026-39124-S1982, et celui-ci a retenu toute notre attention. Malgré toutes les qualités que présente celui-ci, nous sommes au regret de vous informer que nous ne pouvons donner une suite favorable à votre candidature."]
#candidature_ok = ["Nous avons bien reçu votre candidature et nous la transmettons au recruteur. RTE devrait vous en confirmer la bonne réception et vous contacter directement pour la suite. Soyez préparé si votre candidature est retenue en vous informant sur l'entreprise. Présentation générale, chiffres clés, avantages, actualités, étapes de recrutement.... Partez à la pêche aux infos !"]
#
#print(type_retour[model.predict(vectorizer.transform(refus))[0] - 1])  # Résultat attendu : [3] (Retour négatif)
#print(type_retour[model.predict(vectorizer.transform(acceptation))[0] - 1])  # Résultat attendu : [1] (acceptation)
#print(type_retour[model.predict(vectorizer.transform(entretien))[0] - 1])  # Résultat attendu : [2] (Entretien)
#print(type_retour[model.predict(vectorizer.transform(candidature_ok))[0] - 1])  # Résultat attendu : [4] (Confirmation candidature)