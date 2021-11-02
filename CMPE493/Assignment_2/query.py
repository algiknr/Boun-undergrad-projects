import pickle
import json
import sys
from prep import TrieNode,Trie


def queryprocess(queryword):
    #in case of any capital letters
    queryword = queryword.casefold()

    #this file has the dictionary of newids for each word
    #we need to get it previously formed file in order to process it
    with open("inverted_index.json", 'r') as jsonfile:
        fetchedinvertedindex = json.load(jsonfile)

    #It will do the single word process which only needs to look json file
    if not queryword[-1]=='*':
        singlewordqueryset=set()
        for singlewordquery in fetchedinvertedindex:
            if singlewordquery==queryword:
                for eachnewid in fetchedinvertedindex[singlewordquery]:
                    singlewordqueryset.add(eachnewid)
        #Print the result
        print(sorted(singlewordqueryset,reverse=False))

    #It will do the single wildcardprocess
    #We need to get all the possible words starting with designated keyword
    #From these words we can fetch NewIds of each word from json file
    if queryword[-1]=='*':
        # this file has the trie data structure formed from the preprocessed articles
        # we need to get it previously formed file in order to process it
        with open("trie.pickle", 'rb') as picklefile:
            fetchedtrie = pickle.load(picklefile)

        wildcarddisplayqueryset=set()
        lookupwords=fetchedtrie.fetchpossiblewords(queryword[:-1])
        for wildcardquery in fetchedinvertedindex:
            for item in lookupwords:
                if item==wildcardquery:
                    for eachnewid in fetchedinvertedindex[wildcardquery]:
                        wildcarddisplayqueryset.add(eachnewid)
        # Print the result
        print(sorted(wildcarddisplayqueryset,reverse=False))


def main(argv):

    # get the keyword from user to search
    querykey = input("Please enter query key: ")

    #take the keyword until it is a proper key word
    while(len(querykey)==0 or querykey=="*"):
        querykey = input("Please don't forget to enter query key: ")

    queryprocess(querykey)


if __name__ == "__main__":
    main(sys.argv[1:])
