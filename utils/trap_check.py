from urllib.parse import urlparse

class TrapCheck:
    def __init__(self):
        self.tracking_url_netloc = ""
        self.tracking_url_path = ""
        self.count = 0

    def urlCount(self, url):
        url_parsed = urlparse(url)
        if (url_parsed.netloc != self.tracking_url_netloc or url_parsed.path != self.tracking_url_path):
            self.tracking_url_netloc = url_parsed.netloc
            self.tracking_url_path = url_parsed.path
            self.count = 1
        else:
            self.count += 1

    def highCount(self):
        if self.count >= 20:
            return True
        else:
            return False

    def returnCount(self):
        return self.count
    
    def is_not_trap_url(self, url):
        url_parsed = urlparse(url)
        return (self.tracking_url_netloc != url_parsed.netloc or
                self.tracking_url_path != url_parsed.path)
