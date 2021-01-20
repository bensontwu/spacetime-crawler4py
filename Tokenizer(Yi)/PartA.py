import re
import argparse

class Tokenizer:

    def __init__(self, file_path: str):
        self.text_file = file_path

    '''
    The tokenize method seems to run in polynomial time as
    each line in the for loop, the line is iterated through
    and split accorindingly before putting it into a list.
    O(n*n) = O(n^2)
    '''
    def tokenize(self):
        self.token_list = []
        temp_list = []
        open_file = open(self.text_file, "r")
        for file_line in open_file:
            alphanum_chars = re.split("[^A-Za-z\d]", file_line)
            temp_list.extend(alphanum_chars)
        open_file.close()
        for i in temp_list:
            if i != '':
                i = i.lower()
                self.token_list.append(i)
        return self.token_list

    '''
    The computeWordFrequencies method seems to run in polynomial time.
    The two for loops would result in a quadratic run time since for every
    loop, another loop is ran. O(n^2)
    '''                                     
    def computeWordFrequencies(self):
        self.map_dict = {}
        for i in self.token_list:
            token_exists = False
            for j, k in self.map_dict.items():
                if j == i:
                    freq = k + 1
                    self.map_dict[j] = freq
                    token_exists = True
            if token_exists == False:
                self.map_dict[i] = 1
        return self.map_dict

    '''
    The printFreq method would most likely be of a logarithmic time complexity
    because of the sorted function from the Python Standard Library. With less
    values, the function can operate relatively quickly but as the number
    of value increases, it takes much more time. 
    '''
    def printFreq(self):
        sorted_tokenFreq = sorted(self.map_dict.items(), key = lambda token: token[1], reverse = True)
        for token, freq in sorted_tokenFreq:
            print(f"{token} {freq}")





def validFile(filePath: str):
    try:
        testFile = open(filePath, "r")
        testFile.close()
        return True
    except:
        return False

def runProgram(user_input: str):
    if validFile(user_input) == True:    
        t = Tokenizer(user_input)
        t.tokenize()
        t.computeWordFrequencies()
        t.printFreq()
    else:
        print("Invalid file name, please try again.")


if __name__ == "__main__":
    commandLine = argparse.ArgumentParser()
    commandLine.add_argument("file", type = str)
    commandLine_input = commandLine.parse_args()
    runProgram(commandLine_input.file)

