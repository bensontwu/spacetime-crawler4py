import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as soup

def tokenize(text):
    token_list = []

    alphanum = nltk.tokenize.RegexpTokenizer()


def scraper(url, resp):
    links = extract_next_links(url, resp)
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):

    urls = list()

    http = requests.get(url).text
    html = soup(http, 'html.parser')

    # find_all(name, keyword)
    # Refer to https://www.crummy.com/software/BeautifulSoup/bs4/doc/#find-all
    for link in html.find_all("a", href=re.compile("^/.")):
        urls.append(url+link["href"])

    print("Numer of pages found: ", len(urls))

    return urls


def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


# urls = ['http://quotes.toscrape.com']

# while len(urls) != 0:

#     url = urls.pop(0)

#     http = requests.get(url).text
#     html = soup(http, 'html.parser')

#     for link in html.find_all("a", href=re.compile("^/.")):
#         print(url+link["href"])

#     urls.pop(0)

# print(urls)