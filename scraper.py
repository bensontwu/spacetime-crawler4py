import re
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup as soup

from bs4.element import Comment


#this is O(N) and linear relative to the size of the input because it iterates trhough each line of the file once
def tokenize(text):
    final_list=[]
    stop_set = set()
    stopFile = open("stop_words.txt","r")
    while True:
        word = stopFile.readline().lower()
        if word == "":
            break
        else:
            stop_set.add(word.strip())
    try:
        while True:
            line = text.readline().lower()
            if line == "":
                break
            else:
                
                temp = re.split("[^A-Za-z0-9']",line)
                for i in temp:
                    if i !="" and i not in stop_set and len(i)>=3:
                        final_list.append(i)
                        
    except FileNotFoundError:
        print("This file doesn't exist.")
        return []
    if final_list ==[]:
        print("This file has no tokens.")
    return final_list


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


# This function return true
# 1. if text element is not comment inside html.
# 2. if text element is not inside invalid html tags.
# Refered to : https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
def elem_check(element):
    if isinstance(element, Comment):
            return False
    
    elif element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
            return False

    return True



urls = ['https://www.ics.uci.edu/community/alumni/']


url = urls.pop(0)

http = requests.get(url).text
html = soup(http, 'html.parser')

texts = html.findAll(text=True)


ext_text = filter(elem_check, texts) 

clean_text = " ".join(t.strip() for t in ext_text)

print(clean_text)