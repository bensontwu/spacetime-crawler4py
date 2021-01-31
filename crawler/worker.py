from os import write
from threading import Thread
from utils.simhash_checker import SimhashChecker

from utils.download import download
from utils.response_validator import ResponseValidator
from utils import get_logger
from utils.invalid_links import write_invalid_links_to_file
from scraper import scraper
import time
# from utils.simhash_check import SimhashCheck
from utils.robots import robot_can_fetch


class Worker(Thread):
    def __init__(self, worker_id, config, frontier, subdomain_printer, tokenizer):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.subdomain_printer = subdomain_printer
        self.tokenizer = tokenizer
        self.unique_urls = 0
        self.simhash_checker = SimhashChecker(config.simhash_threshold)
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")

                # For question 1
                print("--------------------------------------------------")
                print(f"Number of unique urls:\t{self.unique_urls}")
                print("--------------------------------------------------")

                # For question 2
                print("--------------------------------------------------")
                print(f"Url with most content:\t{self.tokenizer.biggest_url}")
                print(f"# of characters:\t{self.tokenizer.most_words}")
                print("--------------------------------------------------")
                break
            resp = download(tbd_url, self.config, self.logger)
            self.logger.info(
                f"Downloaded {tbd_url}, status <{resp.status}>, "
                f"using cache {self.config.cache_server}.")
            
            if not ResponseValidator.is_worth_scraping(resp):
                # skip this url
                # for debugging purposes
                write_invalid_links_to_file([tbd_url], "Failed ResponseValidator")
                continue
            
            if not robot_can_fetch(tbd_url):
                write_invalid_links_to_file([tbd_url], "Failed robot check")
                continue
            
            # Simhash checking
            tokens = self.tokenizer.tokenize(resp)
            hash = self.simhash_checker.get_simhash(tokens)
            near_dups = self.simhash_checker.get_similar_hashes(hash)
            if len( near_dups ) > 0:
                # skip this url
                write_invalid_links_to_file([tbd_url], f"Failed Simhash Check, near dups: {near_dups}")
                self.simhash_checker.add_simhash(tbd_url, hash)
                continue
            self.simhash_checker.add_simhash(tbd_url, hash)
            
            self.unique_urls += 1

            scraped_urls = scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)

            # printing subdomains
            self.subdomain_printer.print_sub_doms_to_file(scraped_urls)

            # printing tokens
            self.tokenizer.print_word_count_to_file(tbd_url, resp)
            self.tokenizer.print_tokens_to_file(resp)

            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
