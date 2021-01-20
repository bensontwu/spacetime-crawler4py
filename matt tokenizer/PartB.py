import PartA
import sys
#O(n) linear relative to size of input because set conversions constant and only one iteration through each line of each file
def fileIntersect(f1,f2):
    f_set = set()
    t1 = set(PartA.tokenize(f1))
    t2 = set(PartA.tokenize(f2))
    for i in t1:
        if i in t2:
            f_set.add(i)
    print(f_set)
    print(len(f_set))
    
#O(n) , runs fileIntersect which is O(n)
#https://docs.python.org/3/library/sys.html
def main():
    try:
        file1 = sys.argv[1]
        file2 = sys.argv[2]
        fileIntersect(file1, file2)
    except IndexError:
        print("Please use two files as input.")
    
if __name__ == "__main__":
    main()
