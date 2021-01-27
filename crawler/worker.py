from threading import Thread

from utils.download import download
from utils.response_validator import ResponseValidator
from utils import get_logger
from utils.invalid_links import write_invalid_links_to_file
from scraper import scraper
import time


class Worker(Thread):
    def __init__(self, worker_id, config, frontier, subdomain_printer, tokenizer):
        self.logger = get_logger(f"Worker-{worker_id}", "Worker")
        self.config = config
        self.frontier = frontier
        self.subdomain_printer = subdomain_printer
        self.tokenizer = tokenizer
        super().__init__(daemon=True)
        
    def run(self):
        while True:
            tbd_url = self.frontier.get_tbd_url()
            if not tbd_url:
                self.logger.info("Frontier is empty. Stopping Crawler.")

                # For question 2
                self.logger.info(f"Biggest url: {self.tokenizer.biggest_url}")
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

            scraped_urls = scraper(tbd_url, resp)
            for scraped_url in scraped_urls:
                self.frontier.add_url(scraped_url)

            # printing subdomains
            self.subdomain_printer.print_sub_doms_to_file(scraped_urls)

            # printing tokens
            self.tokenizer.print_tokens_to_file(resp)

            self.frontier.mark_url_complete(tbd_url)
            time.sleep(self.config.time_delay)
