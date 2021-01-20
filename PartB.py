from PartA import tokenize
# To get path from commandline
import sys

token1 = tokenize(sys.argv[-1])
token2 = tokenize(sys.argv[-2])


# I used referenced to the code written here 
# https://stackoverflow.com/questions/18264471/in-python-how-do-i-find-common-words-from-two-lists-while-preserving-word-order

# Time complexity for set is O(1) because they use hash table
# Reference: https://wiki.python.org/moin/TimeComplexity
common = set(token1)&set(token2)

print("Common words: ", common)
print("Number of common words: ", len(common))




