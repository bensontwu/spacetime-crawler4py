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
		
		if len(parsed.fragment) != 0:
			return False

		if re.match(
			r".*\.(css|js|bmp|gif|jpe?g|ico"
			+ r"|png|tiff?|mid|mp2|mp3|mp4"
			+ r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
			+ r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
			+ r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
			+ r"|epub|dll|cnf|tgz|sha1"
			+ r"|thmx|mso|arff|rtf|jar|csv"
			+ r"|rm|smil|wmv|swf|wma|zip|rar|gz|txt|odc)$", parsed.path.lower()):
			return False
		
		if re.match(
					r"http(s|)://wics\.ics\.uci\.edu/events/\d{4}(-\d+)+." +
					r"|http(s|)://wics\.ics\.uci\.edu/events/category/social-gathering/\d{4}(-\d+)+."+
					r"|http(s|)://wics\.ics\.uci\.edu/events/category/project-meeting/\d{4}(-\d+)+.", url):
			return False

		if re.match(
				r".*\b(\.|)ics\.uci\.edu\b.*" +
				r"|.*\b(\.|)cs\.uci\.edu\b.*" +
				r"|.*\b(\.|)informatics\.uci\.edu\b.*" +
				r"|.*\b(\.|)stat\.uci\.edu\b.*" +
				r"|.*\/\/today\.uci\.edu\/department\/information_computer_sciences\b.*", url):
			return True
			
		import urllib.robotparser

		try:
			# 1. Create RobotFileParser instance
			rp = urllib.robotparser.RobotFileParser()
			# 2. Set URL
			# Robots.txt is always there after the root url
			print(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
			rp.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
			# 3. Read and interpret robots.txt
			rp.read()

			# Return True if the url is allowed to be fetch
			return rp.can_fetch("*", url)

		except urllib.error.URLError:
			print("Robots.txt doesn't exist for ", parsed.scheme + "://" + parsed.netloc)

			return True

	except TypeError:
		print("TypeError for ", parsed)
		raise


# import urllib.robotparser

# def is_valid_url(url):

# 		parsed = urlparse(url)

# 		try:
# 			# 1. Create RobotFileParser instance
# 			rp = urllib.robotparser.RobotFileParser()
# 			# 2. Set URL
# 			# Robots.txt is always there after the root url
# 			print(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
# 			rp.set_url(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
# 			# 3. Read and interpret robots.txt
# 			rp.read()

# 			# Return True if the url is allowed to be fetch
# 			return rp.can_fetch("*", url)

# 		except urllib.error.URLError:
# 			print("Robots.txt doesn't exist for ", parsed.scheme + "://" + parsed.netloc)


urls = ["https://wics.ics.uci.edu/events/", "https://wics.ics.uci.edaaaa/events/", 
"https://www.ics.uci.edu/community/news/", "https://support.ics.uci.edu/robots.txt",
"https://support.ics.uci.edu/"]

# There is error for https://support.ics.uci.edu/robots.txt

for url in urls:
	print(is_valid(url))

# parsed = urlparse(url)

# print(parsed.scheme + "://" + parsed.netloc + "/robots.txt")
# 
# urls = ['https://aa.cs.uci.edu/department/information_computer_sciences',
# 		'https://cs.uci.edu/department/information_computer_sciences',
# 		'https://wics.economicics.uci.edu/events/category/social-gathering/aafa/']
# for url in urls:
# 	print(is_valid(url))


# # ---- How to check if specific URL is allowed to access using robots.txt ---
# import urllib.robotparser

# root_urls = "https://www.ics.uci.edu/robots.txt"
# # robots_url = url + "robots.txt"

# try:
# 	# 1. Create RobotFileParser instance
# 	rp = urllib.robotparser.RobotFileParser()
# 	# 2. Set URL
# 	rp.set_url(robots_url)
# 	# 3. Read and interpret robots.txt
# 	rp.read()

# except urllib.error.URLError:
# 	print("URL Doesn't exist")


# url = "https://www.ics.uci.edu/faculty/"

# # Check if we are able to crawl its url
# # rp.can_fetch(user_agent, url)
# print('*: '+str(rp.can_fetch('*', url)))



# # (1-2)robotsから取得できるか確認
# print('baiduspider: '+ str(rp.can_fetch('baiduspider', url)))




# https://wics.ics.uci.edu/events/2021-01-25/
# https://wics.ics.uci.edu/events/category/social-gathering/2020-05
# https://wics.ics.uci.edu/events/category/project-meeting/2019-04




# urls = ["https://wics.ics.uci.edu/events/category/project-meeting/2019-04",
# "https://wics.ics.uci.edu/events/category/social-gathering/2020-05",
# "https://wics.ics.uci.edu/events/2021-01-08",
# "https://wics.ics.uci.edu/events/2021-01-07",
# "https://wics.ics.uci.edu/events/2021-01-06",
# "https://wics.ics.uci.edu/events/2021-01-05"]

# for url in urls:
# 	res = requests.get(url)
# 	print("Content-length for", url, "is", res.headers['content-length'])


# import time

# import sys
# import requests



# start = timeit.timeit()
# print("hello")
# end = timeit.timeit()
# print(end - start)

# response = requests.get(
#     "https://news.uci.edu/2021/01/25/increasing-ocean-temperature-threatens-greenlands-ice-sheet/%22")

# print(len("a".encode("utf8")))

# import sys
# print(len("helloaaa!".encode("utf8")))

# {'content-length': '944', 'content-disposition': 'attachment; filename="Lab001_A_R03.txt"', 'server': 'Apache-Coyote/1.1', 'connection': 'close', 'date': 'Thu, 19 May 2016 05:04:45 GMT', 'content-type': 'text/plain; charset=UTF-8'}
# >>> int(res.headers['content-length'])





# print(urlparse("https://evoke.ics.uci.edu/hollowing-i-in-the-authorship-of-letters-a-note-on-flusser-and-surveillance/?hello&replytocom=48217#respond"))

# This function return true
# 1. if text element is not comment inside html.
# 2. if text element is not inside invalid html tags.
# Refered to : https://stackoverflow.com/questions/1936466/beautifulsoup-grab-visible-webpage-text
# def elem_check(element):
#     if isinstance(element, Comment):
#             return False
	
#     elif element.parent.name in ['style', 'script', 'head', 'meta', '[document]']:
#             return False

#     return True



# urls = ['https://www.cs.uci.edu/']


# url = urls.pop(0)

# http = requests.get(url).text
# html = soup(http, 'html.parser')

# texts = html.findAll(text=True)


# ext_text = filter(elem_check, texts) 

# clean_text = " ".join(t.strip() for t in ext_text)

# tokens = tokenize(clean_text)

# print(tokens)
