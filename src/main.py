import parseHtml
import callGMail as cgm
import TFIDFmail as tfidf

# Entraîne le modèle
vectorizer, model = tfidf.train_model()

def getMessagesId(n):
    #récupère 20 messages
    results = cgm.service.users().messages().list(
    userId="me",
    maxResults=n
    ).execute()

    list = []

    #met les IDs de chaques message dans une liste
    for item in results.get("messages", []):
        message = cgm.service.users().messages().get(
            userId="me",
            id=item["id"],
            format="full"
        ).execute()

        payload = message.get("payload", {})
        #print(item["id"], payload.get("mimeType"))
        list.append(item["id"])

    return list

def getMessageType(list):
    dico = {}
    for i in range(len(list)):
        decodeMessage = cgm.decode_message_body(cgm.getMessagePayload(list[i]))
        #Parse the HTML content
        parsed_html = parseHtml.parseHtmlMessage(decodeMessage)
        #Type de message
        dico[list[i]] = tfidf.type_retour[model.predict(vectorizer.transform([parsed_html]))[0] - 1]

    return dico



#récupère tous les labels existants
lb = cgm.service.users().labels().list(userId='me').execute().get('labels', [])
#pose les label perso
lb_perso = ["Confirmation candidature", "Entretien", "Retour positif", "Retour négatif", "Autre"]
list_lb_names = [libs['name'] for libs in lb]

#Build les labels nécessaire à l'application
#crée les labels perso si ce n'est pas déjà fait
for lb_perso in lb_perso:
    if lb_perso not in list_lb_names:
        created_label = cgm.service.users().labels().create(userId='me', body={'name': lb_perso}).execute()
        print(f"Libellé créé avec l'ID : {created_label['id']}")
    else:
        print(f"Le libellé '{lb_perso}' existe déjà.")


#récupère les messages OK
n = 10 #nb mail à récupérer
list = getMessagesId(n)

#récupère le type de chaque message et son identifiant OK
dico = getMessageType(list)
#print(dico)

#test pose les labels sur les messages OK
for message_id, label_name in dico.items():
    label_id = cgm.getLabelsIdByName(label_name)
    if label_id:
        cgm.setLabels(message_id, [label_id])
        print(f"Label '{label_name}' appliqué au message ID : {message_id}")
    else:
        print(f"Impossible de trouver l'ID du label '{label_name}' pour le message ID : {message_id}")