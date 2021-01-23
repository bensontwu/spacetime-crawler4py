import re
import sys
#this is O(N) and linear relative to the size of the input because it iterates trhough each line of the file once
def tokenize(TextFilePath):
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
        file = open(TextFilePath,"r")
        while True:
            line = file.readline().lower()
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

#this is O(N) and linear relative to the size of the input because it iterates trhough each token once
def computeWordFrequencies(inList):
    final_dict = {}
    for i in inList:
        if i in final_dict:
            final_dict[i]+=1
        else:
            final_dict[i]=1
    return final_dict
#this is O(nlogn) and linear relative to the size of the input 
# referenced for complexity explanation https://realpython.com/sorting-algorithms-python/
def freqPrint(Frequencies):
    sort_freq = dict(sorted(Frequencies.items(), key = lambda i: (i[1]), reverse = True))
    for k,v in sort_freq.items():
        print(k+"="+str(v))

def main():
    file = sys.argv[1]
    print(tokenize(file))
    freqPrint(computeWordFrequencies(tokenize(file)))
    
if __name__ == "__main__":
    main()


