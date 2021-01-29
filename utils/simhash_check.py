from utils.soup import get_soup
from simhash import Simhash, SimhashIndex
import re

# using simhash: https://github.com/1e0ng/simhash
class SimhashCheck:

    def __init__(self, config):
        self.simhash_index = SimhashIndex([], k = config.simhash_tolerance)
        self.width = config.simhash_width

    def add_hash(self, url, hash) -> None:
        if not hash:
            return
        self.simhash_index.add(url, hash)
    
    def get_near_dups(self, hash) -> list:
        if not hash:
            return []
        return self.simhash_index.get_near_dups(hash)
    
    def get_hash(self, resp) -> Simhash:
        soup = get_soup(resp)
        if soup == None:
            return

        texts = soup.findAll(text=True)
        webpage_text = " ".join(texts)
        hash = Simhash(self._get_features(webpage_text))

        return hash
    
    def _get_features(self, s):
        s = s.lower()
        s = re.sub(r'[^\w]+', '', s)
        return [s[i:i + self.width] for i in range(max(len(s) - self.width + 1, 1))]


        
