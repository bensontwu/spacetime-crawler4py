import PartA
import argparse

class Intersection:
    
    def __init__(self, file_path1: str, file_path2: str):
        self.text1 = file_path1
        self.text2 = file_path2
        self.matched_tokens = 0;

    '''
    The compare function appears to run in polynomial time.
    The for loop takes each key in the first dictionary and
    compare it with the second dictionary. O(n^2)
    '''
    def compare(self):
        t1 = PartA.Tokenizer(self.text1)
        t1.tokenize()
        map1 = t1.computeWordFrequencies()

        t2 = PartA.Tokenizer(self.text2)
        t2.tokenize()
        map2 = t2.computeWordFrequencies()

        for token in map1.keys():
            if token in map2.keys():
                self.matched_tokens += 1

    '''
    printResults is constant since it is
    only printing out the stored integer. 
    '''
    def printResults(self):
        print(self.matched_tokens)




def runProgram(file1: str, file2: str):
    if (PartA.validFile(file1) == True) and (PartA.validFile(file2) == True):    
        i = Intersection(file1, file2)
        i.compare()
        i.printResults()
    else:
        print("One or more invalid file names, please try again.")
    
if __name__ == "__main__":
    commandLine = argparse.ArgumentParser()
    commandLine.add_argument("file1", type = str)
    commandLine.add_argument("file2", type = str)
    commandLine_input = commandLine.parse_args()
    runProgram(commandLine_input.file1, commandLine_input.file2)

