from urllib.parse import urlparse

class trap_check:
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
        if self.count == 20:
            return True
        else:
            return False

    def returnCount(self):
        return self.count


#Testing the class
url_list = ["http://www.ics.uci.edu", "https://www.ics.uci.edu/grad/admissions/index", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/about/search/index.php#ffsf", "https://www.ics.uci.edu/about/search/index.php#fsff", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/about/search/index.php"]

t = trap_check()
print()
print("--Testing urls with the same domain--")
print(f"Number of links in test list: {len(url_list)}")
print()
for i in url_list:
    t.urlCount(i)
    if t.highCount() == True:
        print("20 consecutive links with the same netloc and path. It's a trap!")
        count = t.returnCount()
        print(f"Number of links at stop: {count}")
        break






