import re
from urllib.parse import urlparse

from utils.soup import get_soup
from utils.trap_check import TrapCheck
from utils.invalid_links import write_invalid_links_to_file

MAX_CONTENT_SIZE = 50000

def scraper(url, resp):
    links = extract_next_links(url, resp)
    final_links = []
    invalid_links = []
    for link in links:
        if is_valid(link):
            final_links.append(link)
        else:
            invalid_links.append(link)
    
    # for debugging purposes
    write_invalid_links_to_file(invalid_links, "Failed is_valid check")

    return final_links

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
        
        if len(parsed.fragment) != 0:
            return False

        if re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|txt|odc)$", parsed.path.lower()):
            return False
        
        if re.match(
                    r"http(s|)://wics\.ics\.uci\.edu/events/\d{4}(-\d+)+." +
                    r"|http(s|)://wics\.ics\.uci\.edu/events/category/social-gathering/\d{4}(-\d+)+."+
                    r"|http(s|)://wics\.ics\.uci\.edu/events/category/project-meeting/\d{4}(-\d+)+.", url):
            return False

        return re.match(
                r".*\b(\.|)ics\.uci\.edu\b.*" +
                r"|.*\b(\.|)cs\.uci\.edu\b.*" +
                r"|.*\b(\.|)informatics\.uci\.edu\b.*" +
                r"|.*\b(\.|)stat\.uci\.edu\b.*" +
                r"|.*\/\/today\.uci\.edu\/department\/information_computer_sciences\b.*", url)

    except TypeError:
        print("TypeError for ", parsed)
        raise
