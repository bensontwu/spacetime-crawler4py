import re
from urllib.parse import urlparse

from utils.soup import get_soup
from utils.trap_check import TrapCheck

MAX_CONTENT_SIZE = 50000

def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    soup = get_soup(resp)

    if soup == None:
        return list()

    next_links = []
    trap_check = TrapCheck()
    for link in soup.find_all('a'):
        href = link.get('href')

        # increment the trap checker
        trap_check.urlCount(href)
        if trap_check.highCount():
            # get rid of all of the trap urls
            next_links = list(filter(trap_check.is_not_trap_url, next_links))
            break
        if href != url:
            next_links.append(href)

    return next_links

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        if len(parsed.fragment) != 0 or len(parsed.query) != 0:
            return False

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
                + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower()):
            return False

        return (re.match(r".*((\.|)ics\.uci\.edu|(\.|)cs\.uci\.edu|(\.|)informatics\.uci\.edu|(\.|)stat\.uci\.edu" +
                         r"|today\.uci\.edu/department/information_computer_sciences)", parsed.netloc))
    except TypeError:
        print("TypeError for ", parsed)
        raise
