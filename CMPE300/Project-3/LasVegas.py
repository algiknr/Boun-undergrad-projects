import random

def updateAvailCols(R,board,cols,n):
    tmplist = list(range(0, n))
   #aynı columnda
    for i in cols:
        if i in tmplist:
            tmplist.remove(i)


    for i in range(0,n):
        r = R
        c = i
        #sağ üst çapraz
        while r>=0  and c<n:
            if board[r][c] == 1:
                if i in tmplist:
                    tmplist.remove(i)
            r-=1
            c+=1
        r = R
        c = i
        #sol üst çapraz
        while r>=0 and c>=0 :
            if board[r][c] == 1:
                if i in tmplist:
                    tmplist.remove(i)
            r-=1
            c-=1
    return tmplist
def printBoard(board,n):
    for i in range(n):
        for j in range(n):
            print(board[i][j], end=" ")
        print("\n")
    print("\n")
def isSafe(board,row,col,n):
    for i in range(row):
        if board[i][col]==1:
            return False
    r=row
    c=col
    #sol üst
    while r >= 0 and c >= 0:
        if board[r][c] == 1:
            if board[r][c]==1:
                return False
        r -= 1
        c -= 1
    r = row
    c = col
    #sağ üst
    while r >= 0 and c < n:
        if board[r][c] == 1:
            if board[r][c] == 1:
                return False
        r -= 1
        c += 1
    return True


def QueensLasVegasPart1(n,fileObj):
    board = [[0 for col in range(n)] for row in range(n)]
    columns = list()
    availColumns=list(range(0, n))
    R=0
    steps=0

    while len(availColumns)!=0 and R <n-1:
        C = random.choice(availColumns)
        columns.append(C)
        board[R][C] = 1
        R = R + 1
        availColumns.remove(C)
        availColumns=updateAvailCols(R,board,columns,n)
        steps+=1
        out1 = "Step " + str(steps) + ": Columns: " + str(columns)+"\n"
        fileObj.write(out1)
        out1 = 'Step ' + str(steps) + ': Available: ' + str(availColumns)+"\n"
        fileObj.write(out1)
    if len(availColumns)!=0 and R==n-1:
        C = random.choice(availColumns)
        columns.append(C)
        board[R][C] = 1
        R = R + 1
        steps+=1
        availColumns.clear()
        out1="Step "+ str(steps)+ ': Columns: '+str(columns)+"\n"
        fileObj.write(out1)
        out1='Step '+ str(steps)+ ': Available: '+str(availColumns)+"\n"
        fileObj.write(out1)


    if len(availColumns)==0 and R<=n-1:
        fileObj.write('Unsuccessful\n\n')
        return availColumns
    else:
        fileObj.write('Successful\n\n')
        return columns


def QueensLasVegasforPart2(n,k):
    board = [[0 for col in range(n)] for row in range(n)]
    columns = list()
    availColumns = list(range(0, n))
    R = 0
    steps = 0
    while len(availColumns) != 0 and R < k-1:
        C = random.choice(availColumns)
        columns.append(C)
        board[R][C] = 1
        R = R + 1
        availColumns.remove(C)
        availColumns =updateAvailCols(R, board, columns, n)
        steps += 1
    if len(availColumns) != 0 and R == k - 1:
       C = random.choice(availColumns)
       columns.append(C)
       board[R][C] = 1
       R = R + 1
       steps += 1
       availColumns.clear()
       return board
    return board


def DeterministicPart2(board,row,k,n):
    if(row>=n):
        return True
    for c in range(0,n):
        if isSafe(board,row,c,n):
            board[row][c]=1
            if DeterministicPart2(board,row+1,k,n):
                return True
            board[row][c] = 0
    return False

def isQLSuccessfullPart2(board,n,k):
    if k==0:
        return True
    for j in range(n):
        if board[k-1][j]==1:
            return True
    return False
def isSuccess(board,n):
   for i in range(n):
        if board[n-1][i]==1:
            return True
   return False


n=0
i=0

selectPart = str(input())
if selectPart == 'part1':
    for n in range(6, 11, 2):
        fileName = "results_" + str(n) + ".txt";
        fileObj = open(fileName, "w");
        for a in range(10000):
            if len(QueensLasVegasPart1(n,fileObj)) != 0:
                i = i + 1
        print("Las Vegas Algorithm With n =", n)
        print("Number of successful placements is", i)
        print("Number of trials is 10000")
        print("Probability that it will come to a solution is", i / 10000,"\n")
        i = 0
        fileObj.close()

elif selectPart == 'part2':
    for n in range(6, 11, 2):
        print("--------------- ", n, " ---------------")
        for k in range(0, n):
            for j in range(10000):
                board = QueensLasVegasforPart2(n, k)
                while not isQLSuccessfullPart2(board, n, k):
                    board = QueensLasVegasforPart2(n, k)
                if DeterministicPart2(board, k, k, n):
                    i = i + 1
            print("k is ", k)
            print("Number of successful placements is", i)
            print("Number of trials is 10000")
            print("Probability that it will come to a solution is", i / 10000)
            i = 0


