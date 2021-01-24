import re
from urllib.parse import urlparse

from utils.soup import get_soup

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    soup = get_soup(resp)

    if soup == None:
        return list()

    next_links = []
    for link in soup.find_all('a'):
        href = link.get('href')
        if href != url:
            next_links.append(href)

    return next_links

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        if re.match(
            r"..(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()) is None:

            if (re.match(r".*((\.|)ics\.uci\.edu|(\.|)cs\.uci\.edu|(\.|)informatics\.uci\.edu|(\.|)stat\.uci\.edu" +
                         r"|today\.uci\.edu/department/information_computer_sciences)", url) is not None):
                return True
            return False
        return False

    except TypeError:
        print ("TypeError for ", parsed)
        raise
