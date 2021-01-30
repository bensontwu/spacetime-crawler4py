from collections import Counter
import hashlib

class SimhashChecker:

    def __init__(self, threshold):
        self.hashes = {}
        self.threshold = threshold
    
    def add_simhash(self, url, hash):
        self.hashes[url] = hash
    
    def get_similar_hashes(self, hash) -> list:
        similar_urls = []
        for url, h in self.hashes.items():
            if self.similarity(hash, h) > self.threshold:
                similar_urls.append(url)
        return similar_urls
    
    def get_simhash(self, tokens):
        # list to store tokens(words) in binary format
        # Ex: ['010101','010101']
        binary_tokens = list()

        for token in tokens:
            # Convert token(word) to binary string
            # Ex: "hello" → b'G\xbc\xe5\xc7OX\x9fHg\xdb\xd5~\x9c\xa9\xf8\x08'
            ida = hashlib.md5(token.encode()).digest()

            # list(ida) converts binary string to binary code (decimal) that ranges from 0~255
            # Ex: "hello" →  b'G\xbc\xe5\xc7OX\x9fHg\xdb\xd5~\x9c\xa9\xf8\x08 → [165, 245, 12, 2, 54]
            ida = list(ida)

            # Convert decimal to binary representation consisting of 0 and 1 by f'{i:08b}'
            # Ex: 165 → 0001010010111001 so the list will be something like ['001010010111001', '111010010110001',...]
            lst = [f'{i:08b}' for i in ida]

            # Join each character byte into token byte
            # Ex:['001010010111001', '111010010110001',...] → '001010010111001111010010110001'
            # This will become Ex: hello = '001010010111001111010010110001'
            binary_tokens.append(''.join(lst))

        # Dictionary of binary_tokens and its frequency in token list
        # Ex: {token(word)='001010010111001111010010110001' : frequency=2}
        # This will be used for weights
        freq_dict = dict(Counter(binary_tokens))

        # list of total for each 16 bits
        tot_lst = list()

        total = 0

        # Conduct mathmatical operations
        # If bit is 1, add weight w. If bit is 0, substract weight w.
        # range(0,128) because token is represented as 16 bytes
        for i in range(0, 128):
            for j in range(0, len(binary_tokens)):

                # Decide weight from token frequency
                w = int(freq_dict[binary_tokens[j]])

                # print("weight:", w)
                # print(int(binary_tokens[j][i]))

                if int(binary_tokens[j][i]) == 1:
                    total += w
                else:
                    total -= w

            tot_lst.append(total)

            total = 0

        finger_print = [1 if i > 0 else 0 for i in tot_lst]

        return finger_print

    def similarity(self, sim1, sim2):
        num_same = 0

        # Calculate number of same elements
        # Ex: 0110000000000000 and 0110000000000000 has 16 same elements
        for i in range(0, 128):
            if sim1[i] == sim2[i]:
                num_same += 1
        # print(num_same)

        return num_same/128
