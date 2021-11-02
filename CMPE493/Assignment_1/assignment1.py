import numpy as np

#this function is for determining the necessary operations to obtain minimum distance
def levenshtein_get_ops(string1, string2, dist_matrix):

    i, j = dist_matrix.shape
    i -= 1
    j -= 1

    ops = list()

    #loop through the whole matrix until index go out
    while i != -1 and j != -1:

        #logic is to back track the left,up and the diagonal
        #because we actually know which operation must have been performed by that info
        #We have to always go to the minimum distance cost
        index = np.argmin([dist_matrix[i-1, j-1], dist_matrix[i, j-1], dist_matrix[i-1, j]])

        #copy-replace check
        if index == 0:
            #this if statement is to check whether it is a replacement or a copy
            #because both of them control through the diogonal
            #difference is that one has a cost effecting the distance so we can check
            if dist_matrix[i, j] > dist_matrix[i-1, j-1]:

                    ops.insert(0, ("cost: 1",'op: replace',"input: "+string1[i-1],"output: "+string2[j-1]))
            else:
                #this if statement is to prevent out of bound
                if i-1 != -1 and j-1 != -1:
                    ops.insert(0, ("cost: 0",'op: copy',"input: "+string1[i-1],"output: "+string2[j-1]))
            i -= 1
            j -= 1

        #insert check
        elif index == 1:

            ops.insert(0, ("cost: 1",'op: insert',"input: "+'*',"output: "+string2[j-1]))
            j -= 1

        #delete check
        elif index == 2:

            ops.insert(0, ("cost: 1",'op: delete',"input: "+string1[i-1],"output: "+'*'))
            i -= 1

    return ops

#this function is nearly same with levenstein_get_ops only diffence is the transpostion check
def damerau_get_ops(string1, string2, dist_matrix):

    i, j = dist_matrix.shape
    i -= 1
    j -= 1

    ops = list()

    while i != -1 and j != -1:

        #we have to check for adjacent transpositions
        if i > 1 and j > 1 and string1[i-1] == string2[j-2] and string1[i-2] == string2[j-1]:
            if dist_matrix[i-2, j-2] < dist_matrix[i, j]:
                ops.insert(0, ("cost: 1",'op: transpose',"change between: "+string2[i-1]+','+string2[i-2]))
                i -= 2
                j -= 2

        index = np.argmin([dist_matrix[i-1, j-1], dist_matrix[i, j-1], dist_matrix[i-1, j]])

        # copy-replace check
        if index == 0:

            if dist_matrix[i, j] > dist_matrix[i-1, j-1]:

                    ops.insert(0, ("cost: 1",'op: replace',"input: "+string1[i-1],"output: "+string2[j-1]))
            else:
                if i-1 != -1 and j-1 != -1:
                    ops.insert(0, ("cost: 0",'op: copy',"input: "+string1[i-1],"output: "+string2[j-1]))
            i -= 1
            j -= 1

        #inset check
        elif index == 1:

            ops.insert(0, ("cost: 1",'op: insert',"input: "+'*',"output: "+string2[j-1]))
            j -= 1

        # delete check
        elif index == 2:

            ops.insert(0, ("cost: 1",'op: delete',  "input: "+string1[i-1],"output: "+'*'))
            i -= 1

    return ops

# this function basically creates an empty matrix according to the lengths of strings
# fills them according to the minimum operation according to the costs
#insert,delete,replace have cost 1 and copy is cost 0
def levenshtein_distance(s1, s2):
    lens1 = len(s1)
    lens2 = len(s2)
    levenshteinmatrix = np.zeros((lens1 + 1, lens2 + 1), dtype=int)

    for i in range(lens1 + 1):
        levenshteinmatrix[i, 0] = i

    for j in range(lens2 + 1):
        levenshteinmatrix[0, j] = j

    for i in range(lens1):
        for j in range(lens2):
            #this check is to determine whether it is replace or a copy
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            levenshteinmatrix[i + 1, j + 1] = min(levenshteinmatrix[i, j + 1] + 1,  # insert
                                  levenshteinmatrix[i + 1, j] + 1,  # delete
                                  levenshteinmatrix[i, j] + cost)  # replace

    return levenshteinmatrix

#this is same with above levinstein_distance function only difference is the transpositional operation check
#transpositional operation check has a cost 1 like delete,replace and insert
def damerau_levenshtein_distance(s1, s2):
    lens1 = len(s1)
    lens2 = len(s2)
    dameraulevenshteinmatrix = np.zeros((lens1 + 1, lens2 + 1), dtype=int)

    for i in range(lens1 + 1):
        dameraulevenshteinmatrix[i, 0] = i

    for j in range(lens2 + 1):
        dameraulevenshteinmatrix[0, j] = j

    for i in range(lens1):
        for j in range(lens2):
            if s1[i] == s2[j]:
                cost = 0
            else:
                cost = 1
            dameraulevenshteinmatrix[i+1, j+1] = min(dameraulevenshteinmatrix[i, j+1] + 1, # insert
                              dameraulevenshteinmatrix[i+1, j] + 1, # delete
                              dameraulevenshteinmatrix[i, j] + cost) # replace

            if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
                dameraulevenshteinmatrix[i+1, j+1] = min(dameraulevenshteinmatrix[i+1, j+1], dameraulevenshteinmatrix[i-1, j-1] + cost) # transpose

    return dameraulevenshteinmatrix


#below function is the main function which display main information for
#levenstein and damerau levinst distance information
#as giving distance,the matrix and the occuring operations for each

if __name__ == "__main__":

    string1 = input('Enter first string :')
    string2 = input('Enter second string :')

    print("")

    print('LEVENSTEIN INFO')
    dist_matrix = levenshtein_distance(string1, string2)
    print("")
    print('Levenshtein Distance : ',end="")
    print(dist_matrix[len(string1)][len(string2)])
    print("")
    print("Levenshtein Matrix : ")
    print("")
    print(dist_matrix)
    print("")
    print("Levenshtein Operations : ")
    print("")
    ops = levenshtein_get_ops(string1, string2, dist_matrix)
    print(ops)

    print("")
    print("------------------")
    print("")

    print('DAMERAU LEVENSTEIN INFO')
    dist_matrix = damerau_levenshtein_distance(string1, string2)
    print("")
    print('Damerau Levenshtein Distance : ',end="")
    print(dist_matrix[len(string1)][len(string2)])
    print("")
    print('Damerau Levenshtein Matrix : ')
    print("")
    print(dist_matrix)
    print("")
    print("Damerau Levenshtein Operations : ")
    print("")
    ops = damerau_get_ops(string1, string2, dist_matrix)
    print(ops)

