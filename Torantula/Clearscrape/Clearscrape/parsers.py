from urlparse import urlparse

def parse_site_components(item):
    """
    Returns full HTML, URL, and the top-level domain name from a Site item.

    :param item: The Site object passed by the spider
    :return: text, url, domain, links
    """

    text = item['body']
    url = urlparse(item['url'])
    domain = url.netloc
    # Creates a list of unique links from a domain (for graphing)
    links = list(set([urlparse(link).netloc for link in item['links']]))
    return text, url, domain, links

def has_keyword(text):
    """
    Returns True if certain content keywords are present in a page text

    :param text: the UTF-8 encoded text from siteComponents
    :return:
    """

    # Because pipeline is inserting pagetexts several directories deeper
    t = open("../../../keywords.txt", "r")
    keywords = [term.strip() for term in t.readlines()]
    t.close()

    for word in keywords:
        try:
            if text[0].lower().find(word) != -1:
                return True
        except IndexError:  # No page text returned
            return False
    return False
