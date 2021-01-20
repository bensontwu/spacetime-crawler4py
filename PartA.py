# Regular expression
import re
# To get path from command line
import sys

# Explanation: This function takes one sentence and tokenize it into the list of words.

# Assumption: I let all values other than alphabet and number to be space except for some
# special characters speciefied [',-.@/]. So, words like "sister-in-law" will be "sisterinlaw"
# to preserve meanings. This is done so that we can match the user who is interested in "sister-in-law".
# I kept differentiated plural and single verb such as "don't" and "doesn't".
# This is because developers can make more different analysis if we let them as they are.
# For example, developers can analyze whether writers of text are denying a third person or themselves
# from the frequency of "doesn't" and "don't". 

# Plus, if the developers desire to put "doesn't" and "don't" together,
# they can do it later in their analysis. From these reasons, I didn't put
# plural and single verb as same.

# I also didn't separate city name and person name such as "San Francisco" to "San" and "Francisco"
# and "Donald Trump" to "DonaldTrump" because it loses meaning. There can be multiple "Donald" for the first name.
# Of course, it may also compress some meaningless words such as "General Information" to "generalinformation", but
# I thought the advantage to do this surpasses the disadvantages of not doing it
# because there are more words that are person's name and city name.

 
# This function tokenize the sentence.
# Time complexity is O(n) because we look through text once for regex.
def tokenize(path):

	f = open(path, "r")
	text = f.read()

	# This is for person name and city name such as "San Francisco" → "SanFrancisco"
	# I made use of this website to create complicated regex pattern
	# https://rubular.com/r/Hguo19BE7X
	text = re.sub('([A-Z][a-z]+)\s([A-Z][a-z]+)', '\\1\\2 ', text)

	# This is for three spaces such as "Donald Trump Jr." → "DonaldTrumpJr."
	text = re.sub('([A-Z][a-z]+)\s([A-Z][a-z]+)\s([A-Z][a-z]+)', '\\1\\2\\3 ', text)


	# Replace special characters
	# @ is for email and / is for url.
	text = re.sub('[\',\.-@/]', '', text)

	# Substitute any characters other than alphabet and number
	text = re.sub('[^a-zA-Z0-9]', ' ', text.lower())

	return text.split()


# Explanation: This function takes one list of words and count their occurence into dictionary.

# Time complexity : O(n)
def computeWordFrequencies(lst):
	
	# Using dictionary comprehension and built-in counter() function
	# Reference: https://stackoverflow.com/questions/2161752/how-to-count-the-frequency-of-the-elements-in-an-unordered-list

	# Time complexity is O(n) because count() is O(n) and dictionary comprehention is O(n)
	# Reference for O(n) in count function: https://github.com/python/cpython/blob/master/Objects/listobject.c
	d = {i:lst.count(i) for i in lst}

	return d

# Explanation: This function takes dictionary and print frequency for each token

# O(n + nlog2n)
def print_freq(freq):

	# Using buit-in sorted function
	# Time complexity is nlog2n time because sorted() uses Timsort.
	sorted_freq = sorted(freq.items(), key=lambda item: item[1], reverse=True)

	# O(n) 
	for d in sorted_freq:
		print(d[0]," => ",d[1])


if __name__ == '__main__':

	# Take the last argument as path
	path = sys.argv[-1]

	lst_tokens = tokenize(path)

	frequencies = computeWordFrequencies(lst_tokens)

	print_freq(frequencies)


