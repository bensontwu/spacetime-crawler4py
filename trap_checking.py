from urllib.parse import urlparse

class trap_check:
    def __init__(self):
        self.tracking_url = ""
        self.count = 0
        
    def urlCount(self, url):
        url_parsed = urlparse(url)
        if url_parsed.netloc != self.tracking_url:
            if self.tracking_url == "":
                self.tracking_url = url_parsed.netloc
                self.count += 1
            else:
                self.tracking_url = url_parsed.netloc
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

#There are 27 links in the url_list with the same authority, it should stop at 20.
url_list = ["http://www.ics.uci.edu", "https://www.ics.uci.edu/grad/admissions/index", "https://www.ics.uci.edu/about/search/index.php",
            "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/",
            "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/",
            "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/",
            "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/",
            "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/",
            "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/",
            "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/community/alumni/", "https://www.ics.uci.edu/grad/admissions/index",
            "https://www.ics.uci.edu/grad/admissions/index", "https://www.ics.uci.edu/grad/admissions/index", "https://www.ics.uci.edu/grad/admissions/index"]

t = trap_check()

for i in url_list:
    t.urlCount(i)
    if t.highCount() == True:
            print("It's a trap!")
            count = t.returnCount()
            print(f"Number of pages at stop: {count}")
            break


    


   
    
