import re
from simhash import Simhash, SimhashIndex
from utils.soup import get_soup
import requests
from utils.response import Response
from bs4 import BeautifulSoup as bs4

def get_features(s):
    width = 3
    s = s.lower()
    s = re.sub(r'[^\w]+', '', s)
    return [s[i:i + width] for i in range(max(len(s) - width + 1, 1))]

def get_hash(resp):
    page_text = resp.text
    soup = bs4(page_text, 'html.parser')

    texts = soup.findAll(text=True)
    webpage_text = " ".join(texts)

    return Simhash(get_features(webpage_text))

def download(url):
    # host, port = config.cache_server
    # resp = requests.get(
    #     f"http://{host}:{port}/",
    #     params=[("q", f"{url}"), ("u", f"{config.user_agent}")])
    # if resp:
    #     return Response(cbor.loads(resp.content))
    resp = requests.get(url)
    return resp

if __name__ == "__main__":

    sim_dex = SimhashIndex([], k=3)

    url = "https://www.ics.uci.edu/about/"
    resp = download(url)
    hash = get_hash(resp)
    sim_dex.add(url, hash)

    print( sim_dex.get_near_dups(hash) )

    

    # print(Simhash('aa').distance(Simhash('bb')))
    # print(Simhash('aa').distance(Simhash('ab')))
    # print(Simhash('aa').distance(Simhash('aa')))

    # data = {
    #     1: u'How are you? I Am fine. blar blar blar blar blar Thanks.',
    #     2: u'How are you i am fine. blar blar blar blar blar than',
    #     3: u'This is simhash test.',
    # }

    # objs = [(str(k), Simhash(get_features(v))) for k, v in data.items()]
    # index = SimhashIndex(objs, k=3)

    # print(index.bucket_size())

    # s1 = Simhash(get_features(
    #     u'How are you i am fine. blar blar blar blar blar thank'))
    # print(index.get_near_dups(s1))

    # index.add('4', s1)
    # print(index.get_near_dups(s1))
