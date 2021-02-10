import json
import psutil
import pickle


def store_index(documents, token_freq):

	inv_idx = {}

	file_num = 0
	docID = 0

	for document in documents:

		for token in document:

			print(token)
			print(token_freq[token])


			if token in inv_idx:
				inv_idx[token].append([docID,token_freq[token]])
			else:
				inv_idx[token] = [[docID, token_freq[token]]]

		docID+=1

		# Used for RAM Check. Turned off for now.
		# if psutil.virtual_memory().percent > 95:

		# Sort by dictionary keys alphabetically
		inv_idx = sorted(inv_idx.items())

		with open('inv' + str(file_num) + '.pickle', 'wb') as f:
			pickle.dump(inv_idx, f)

		inv_idx = {}
		file_num+=1


# Test
documents = [['word', 'in4matx'], ['abcd', 'indexaa']]
token_freq = {'word':3, 'in4matx':5, 'abcd':5, 'indexaa':3}

store_index(documents, token_freq)




