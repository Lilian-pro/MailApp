import parseHtml
import callGMail as cgm
import TFIDFmail as tfidf

from googleapiclient.discovery import build


if __name__ == "__main__":

    

    #récupère tous les labels existants
    lb = cgm.service.users().labels().list(userId='me').execute().get('labels', [])
    #pose les label perso
    lb_perso = ["Confirmation candidature", "Entretien", "Retour positif", "Retour négatif"]
    list_lb_names = [libs['name'] for libs in lb]

    #Build les labels nécessaire à l'application
    #crée les labels perso si ce n'est pas déjà fait
    for lb_perso in lb_perso:
        if lb_perso not in list_lb_names:
            created_label = cgm.service.users().labels().create(userId='me', body={'name': lb_perso}).execute()
            print(f"Libellé créé avec l'ID : {created_label['id']}")
        else:
            print(f"Le libellé '{lb_perso}' existe déjà.")

    


    print("\n--- Messages ---")
    
    #récupère 5 messages
    results = cgm.service.users().messages().list(
    userId="me",
    maxResults=5
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

    #text brut
    decodeMessage = cgm.decode_message_body(cgm.getMessagePayload(list[0]))
    print(f"\n--- Contenu du message {list[0]} ---\n{decodeMessage}\n")
    #test classification TFIDF

    print("\n--- Classification TFIDF ---")
    print(tfidf.type_retour[tfidf.model.predict(tfidf.vectorizer.transform([decodeMessage]))[0] - 1])

    print("\n--- Messages ---")
    #text html
    decodeMessage = cgm.decode_message_body(cgm.getMessagePayload(list[1]))
    #Parse the HTML content
    parsed_html = parseHtml.parse_html_message(decodeMessage)
    print(f"\n--- Contenu parsé du message {list[1]} ---\n{parsed_html}\n")
