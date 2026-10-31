from bs4 import BeautifulSoup

def parseHtmlMessage(html):
    """Conserve le texte et les URLs d'un message HTML."""
    soup = BeautifulSoup(html, "html.parser")

    for element in soup(["style", "script", "noscript", "template", "svg"]):
        element.decompose()

    for element in soup.find_all(True):
        element.attrs.pop("style", None)
        element.attrs.pop("class", None)
        element.attrs.pop("id", None)

    for link in soup.find_all("a", href=True):
        url = link["href"].strip()
        link_text = link.get_text(" ", strip=True)
        link.replace_with(f"{link_text} ({url})" if link_text else url)

    return soup.get_text("\n", strip=True)


