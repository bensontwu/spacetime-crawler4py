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


# def is_valid(url):
#     try:
#         parsed = urlparse(url)
#         if parsed.scheme not in set(["http", "https"]):
#             return False
#         return ((re.match(
#             r"..(css|js|bmp|gif|jpe?g|ico"
#             + r"|png|tiff?|mid|mp2|mp3|mp4"
#             + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
#             + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
#             + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
#             + r"|epub|dll|cnf|tgz|sha1"
#             + r"|thmx|mso|arff|rtf|jar|csv"
#             + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower() is None)))

#         # and (re.match(r"..(ics.uci.edu|cs.uci.edu|informatics.uci.edu|stat.uci.edu" +
#         #                 r"|today.uci.edu/department/information_computer_sciences)", url) is not None))

#     except TypeError:
#         print ("TypeError for ", parsed)
#         raise


def is_valid(url):
	try:
		parsed = urlparse(url)
		if parsed.scheme not in set(["http", "https"]):
			return False

		if len(parsed.fragment) != 0 | len(parsed.query) != 0:
			return False

		if re.match(
			r".*\.(css|js|bmp|gif|jpe?g|ico"
			+ r"|png|tiff?|mid|mp2|mp3|mp4"
			+ r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
			+ r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
			+ r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
			+ r"|epub|dll|cnf|tgz|sha1"
			+ r"|thmx|mso|arff|rtf|jar|csv"
			+ r"|rm|smil|wmv|swf|wma|zip|rar|gz|txt|odc)$", parsed.path.lower()) is None:

			if re.match(r"http(s|)://wics\.ics\.uci\.edu/events/\d{4}(-\d+)+." +
						r"|http(s|)://wics\.ics\.uci\.edu/events/category/social-gathering/\d{4}(-\d+)+."+
						r"|http(s|)://wics\.ics\.uci\.edu/events/category/project-meeting/\d{4}(-\d+)+.", url) is not None:
				return False


			if (re.match(r".*(\b(\.|)ics\.uci\.edu\b|\b(\.|)cs\.uci\.edu\b" +
							r"|\b(\.|)informatics\.uci\.edu|(\.|)stat\.uci\.edu\b" +
							r"|\btoday\.uci\.edu/department/information_computer_sciences\b)", url) is not None):

				return True

			return False

		if requests.head(url).headers['content-length'] > 300000:
			return False

		return False

	except TypeError:
		print ("TypeError for ", parsed)
		raise

urls = ['https://wics.ics.uci.edu/events/2021-01-25', 'https://wics.ics.uci.edu/events/category/social-gathering/2020-05',
		'https://wics.ics.uci.edu/events/category/project-meeting/2019-04', 'https://wics.ics.uci.edu/events/category/project-meeting']

for url in urls:
	print(is_valid(url))


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
