from bs4.element import Comment
from utils.soup import get_soup

import re
import os

class Tokenizer:
    def __init__(self, config, restart: bool):
        self.config = config
        self.stop_set = self._gen_stop_set(config)

        # remove the tokens file from the last run
        if os.path.exists(config.tokens_file) and restart:
            os.remove(config.tokens_file)
    
    # takes response object and prints tokens to file
    def print_tokens_to_file(self, resp) -> list:
        with open(self.config.tokens_file, "a") as file:
            for token in self._tokenize(resp):
                file.write(token + " ")
    
    # Takes response object and generates a list of tokens
    def _tokenize(self, resp) -> list:
        final_tokens = []

        soup = get_soup(resp)
        if soup == None:
            return final_tokens

        texts = soup.findAll(text=True)
        visible_texts = filter(self._elem_check, texts)
        for text in visible_texts:
            line = text.lower()
            tokens = re.split("[^A-Za-z0-9']", line)
            tokens = filter(self._is_valid, tokens)
            final_tokens.extend(tokens)
        return final_tokens

    # generates stop set 
    def _gen_stop_set(self, config):
        stop_set = set()
        with open(config.stop_words, "r") as stop_file:
            while True:
                word = stop_file.readline().lower()
                if word == "":
                    break
                else:
                    stop_set.add(word.strip())
        return stop_set

    # tests if token is valid
    def _is_valid(self, token):
        return token != "" and token not in self.stop_set and len(token) >= 3

    # This function return true
    # 1. if text element is not comment inside html.
    # 2. if text element is not inside invalid html tags.
    # Refered to : https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text

    def _elem_check(self, element):
        if isinstance(element, Comment):
            return False
        elif element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
            return False
        return True