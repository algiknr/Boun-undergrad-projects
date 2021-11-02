import os
import sys
import string
import re
import pickle
import json

class TrieNode:
    #This class will create the each trie node objects

    def __init__(self, character):
        # the character stored in this node
        self.char = character

        # whether this can be the end of a word
        self.is_end = False

        # a dictionary for all the child trienodes( keys are characters, values are trienodes )
        self.children = {}

class Trie():
    #Trie object

    def __init__(self):
        #Trienode is the starting node
        #it won't store any character
        self.root = TrieNode("")

    #used method to fill trie
    def insert(self, keyword):
        """Insert a word into the trie"""
        trienode = self.root

        # Going through the all characters in the keyword
        for character in keyword:
            # Look if there is a child,move to that trienode
            if character in trienode.children:
                trienode = trienode.children[character]
            else:
                # If a character is not found,form a newtrienode in the trie
                newtrienode = TrieNode(character)
                trienode.children[character] = newtrienode
                trienode = newtrienode

        # Mark the end of the each keyword
        trienode.is_end = True

    # Below methods (fetchpossiblewords,dfs) are designed for the outside access from query.py
    #in order to achieve queryprocess they will traverse the Trie object.

    def depthfirstsearch(self, trienode, pref):
        #depth first search algorithm
        #it will go down until see the end trienode to extract the words.

        if trienode.is_end:
            self.output.append((pref + trienode.char))

        for child in trienode.children.values():
            self.depthfirstsearch(child, pref + trienode.char)

    def fetchpossiblewords(self, wordprefix):

        # Use an array within the class to keep all possible outputs
        # because for each prefix there can be many combinations
        self.output = []
        trienode = self.root

        # Check if the wordprefix is in the trie
        for char in wordprefix:
            if char in trienode.children:
                trienode = trienode.children[char]
            else:
                # if can't find the wordprefix, return empty list
                return []

        # Traverse the trie to get all candidates by the dept first search algorithm
        #This will fill up the all possible outputs.
        self.depthfirstsearch(trienode, wordprefix[:-1])

        # Sort the all possible result outputs
        return self.output

def triefinal(lists):
    #create trie object
    t = Trie()

    # Construct trie by adding all the words as keys
    for klist in lists:
        for keys in klist:
            t.insert(keys)

    #store this object as a pickle file
    with open("trie.pickle",'wb') as picklefile:
        pickle.dump(t,picklefile)

def invertedindex(ids,lists):

    #initialize dictionary structure
    dict = {}

    #this loop wil fill out the dictionary taking each new word(item) as keys,
    #and add every occurance index(which is NewIds) to valuelist if it is a new value for that word(item).
    for i in range(len(ids)):
        for item in lists[i]:
            if item not in dict:
                dict[item] = []

            if item in dict:
                if not i in dict[item]:
                    dict[item].append(i)

    # store the dictionary list as a json file
    with open("inverted_index.json", 'w') as jsonfile:
        json.dump(dict, jsonfile)


def preprocess():
    # datatitlebody will store all the info from title and bodyy tags
    datatitlebody=[]
    # creating a dictionary for stopwords
    stopworddict=[]

    #filling stopworddict with stopwordsfile
    with open('stopwords') as f:
        for word in f:
            a=word.splitlines()
            stopworddict.append(a[0])

    # storage to hold the newIds
    ids=[]

    # reading files as well formatted
    for file in os.listdir('reuters21578'):
        # open 'reut2-XXX.sgm' file from /reuters21578 directory
        data = open(os.path.join(os.getcwd(), "reuters21578", file), 'r')
        text = data.read()


        datanewid=[]
        # accessing the NewId numbers
        regex = 'NEWID=(.+?)</TEXT>'
        pattern = re.compile(regex,re.DOTALL)
        datanewid=re.findall(pattern, text)

        #will loop as much as the number of articles
        count= len(datanewid)


        for m in range(count):
            id=datanewid[m].split('">')
            ids.append(id[0].split('"')[1])
            #after accessing the id numbers it will access the
            #content of titles and bodies, will store each of them seperately
            regex2 = '<TITLE>(.+?)</TITLE>'
            pattern2=re.compile(regex2,re.DOTALL)
            # will find every possible title
            matchtitle=re.findall(pattern2,datanewid[m])
            regex3 = '<BODY>(.+?)</BODY>'
            pattern3 = re.compile(regex3, re.DOTALL)
            # will find every possible body
            matchbody = re.findall(pattern3, datanewid[m])

            # if there is no title or body in that id take it as empty
            if matchtitle==[] and matchbody==[]:
                datatitlebody.append([])
            else:
                #do the punctuation removals for title and body
                for punc in string.punctuation:
                    if not matchtitle==[]:
                        matchtitle[0]=matchtitle[0].replace(punc, " ")
                    if not matchbody==[]:
                        matchbody[0] = matchbody[0].replace(punc, " ")

                #do the tokenization seperating each word when see white space
                #before doing the tokenization also do the case-folding
                if not matchtitle == []:
                    matchtitle[0] = matchtitle[0].lower()
                    titlefinalversion = re.findall(r"\w+|[^\w\s]", matchtitle[0], re.UNICODE)

                    # will do the stop word removal
                    for word in list(titlefinalversion):  # iterating on a copy since remove will effect the titlefinalversion
                        if word in stopworddict:
                            titlefinalversion.remove(word)
                else:
                    #if there is nothing to seperate just give as empty
                    titlefinalversion=[]

                # do the tokenization seperating each word when see white space
                # before doing the tokenization also do the case-folding
                if not matchbody == []:
                    matchbody[0]=matchbody[0].lower()
                    bodyfinalversion = re.findall(r"\w+|[^\w\s]", matchbody[0], re.UNICODE)

                    # will do the stop word removal
                    for word in list(bodyfinalversion):  # iterating on a copy since remove will effect the titlebodyversion
                        if word in stopworddict:
                            bodyfinalversion.remove(word)
                else:
                    # if there is nothing to seperate just give as empty
                    bodyfinalversion=[]

                # at the end of each iteration concetenate the title and body information
                datatitlebody.append(titlefinalversion+bodyfinalversion)

        #finish reading the file
        data.close()

    #giving all the extracted title and body information to create a trie structure
    triefinal(datatitlebody)
    # giving all the extracted title and body information along with the NewIds to create a invertedindex structure
    invertedindex(ids,datatitlebody)

def main(argv):

    # starting preprocessing
    preprocess()


if __name__ == "__main__":
    main(sys.argv[1:])
