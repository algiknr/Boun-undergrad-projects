# Yağmur Selek – 2017400273
# Algı Kanar - 2016400123
# Compiling
# Working
# Checkered

# self explanatory variables and comments are included further necessary details are in the report.

from mpi4py import MPI
import numpy as np
import sys as sys
import math as math

# read txt
fileObj = open((sys.argv[1]), "r")
elements = fileObj.read().splitlines()
fileObj.close()

board_len = int(elements[0].split(" ")[0])
wave_num = int(elements[0].split(" ")[1])
object_num = int(elements[0].split(" ")[2])

elements.pop(0)

board_list = []

# fill board_list with towers 2.8(plus tower with health 8) 1.6(circle tower with health 6)
for j in range(0, wave_num):

    empty = np.zeros((board_len, board_len))
    circle = elements[0].split(", ")
    plus = elements[1].split(", ")

    for i in range(0, object_num):
        circle_index_X = int(circle[i].split(" ")[0])
        circle_index_Y = int(circle[i].split(" ")[1])
        empty[circle_index_X][circle_index_Y] = 1.6

        plus_index_X = int(plus[i].split(" ")[0])
        plus_index_Y = int(plus[i].split(" ")[1])
        empty[plus_index_X][plus_index_Y] = 2.8

    board_list.append(empty)
    elements.pop(0)
    elements.pop(0)

# initialize MPI and fetch input file content
comm = MPI.COMM_WORLD
rank = comm.Get_rank()
p = comm.Get_size()
workers_total_num = p - 1
c = int(math.sqrt(workers_total_num))
width = board_len
worker_size_val = int(width / c)
iteration = 8

# manager
if rank == 0:

    # initialize empty board
    board = np.zeros((board_len, board_len))

    # put board_list information to each designated rank worker
    # consequently each rank will obtain a list of divided boards made from each wave configuration
    # the division dimensions will be in worker size value square.

    for i in range(0, workers_total_num):
        message = []
        for j in range(0, wave_num):
            message.append(
                board_list[j][int(i / c) * worker_size_val: int(i / c) * worker_size_val + worker_size_val,
                (i % c) * worker_size_val: (i % c) * worker_size_val + worker_size_val])
        comm.send(message, dest=i + 1)

    # get all the sub_boards back together
    for i in range(0, workers_total_num):
        board[int(i / c) * worker_size_val: int(i / c) * worker_size_val + worker_size_val,
        (i % c) * worker_size_val: (i % c) * worker_size_val + worker_size_val] = comm.recv(source=i + 1)

    # put final board into output file
    with open(sys.argv[2], 'w+') as f:
        for i in range(0, width):
            for j in range(0, width):
                if int(str(float(board[i][j])).split(".")[0]) == 2:
                    f.write("+")
                elif int(str(float(board[i][j])).split(".")[0]) == 1:
                    f.write("o")
                elif int(str(float(board[i][j])).split(".")[0]) == 0:
                    f.write(".")
                if not j==width-1:    
                    f.write(" ")
            if not i==width-1:        
                f.write("\n")

# workers
else:
    # receive sub_board_list
    sub_board_list = comm.recv(source=0)

    # sub_board initialized with first wave sub_board
    sub_board = sub_board_list[0]

    # these are for marking the rank according to their location
    edge_up = False
    edge_down = False
    edge_right = False
    edge_left = False
    edge_up_left = False
    edge_up_right = False
    edge_down_left = False
    edge_down_right = False

    # mark edge up case
    up_neighbour = rank - c
    if up_neighbour < 1:
        up_neighbour = rank + c * (c - 1)
        edge_up = True

    # mark edge down case
    down_neighbour = rank + c
    if down_neighbour > workers_total_num:
        down_neighbour = down_neighbour % workers_total_num
        edge_down = True

    # mark edge left case
    left_neighbour = rank - 1
    if left_neighbour % c == 0:
        left_neighbour = rank + c - 1
        edge_left = True

    # mark edge right case
    right_neighbour = rank + 1
    if right_neighbour % c == 1:
        right_neighbour = rank - c + 1
        edge_right = True

    # mark edge up left diagonal case
    up_left_neighbour = up_neighbour - 1
    if up_left_neighbour % c == 0:
        edge_up_left = True
        up_left_neighbour = up_left_neighbour + c

    # mark edge down left diagonal case
    down_left_neighbour = down_neighbour - 1
    if down_left_neighbour % c == 0:
        edge_down_left = True
        down_left_neighbour = down_left_neighbour + c

    # mark up right diagonal case
    up_right_neighbour = up_neighbour + 1
    if up_right_neighbour % c == 1:
        edge_up_right = True
        up_right_neighbour = up_right_neighbour - c

    # mark down right diagonal case
    down_right_neighbour = down_neighbour + 1
    if down_right_neighbour % c == 1:
        edge_down_right = True
        down_right_neighbour = down_right_neighbour - c

    for fight_round in range(0, iteration * wave_num):

        # sub_board is copied to prevent computations from affecting each other
        # the decisions are made according to the board of previous step

        new_board = sub_board.copy()

        # after the first wave iteration finishes new pieces are going to be added into board in each new wave
        if not (fight_round == 0) and fight_round % iteration == 0:
            for i in range(0, len(sub_board[0])):
                for j in range(0, len(sub_board[0])):
                    if sub_board[i][j] == 0.0:
                        sub_board[i][j] = sub_board_list[int(fight_round / iteration)][i][j]

        empty_grid = np.zeros((len(sub_board[0]), len(sub_board[0])))

        # communication between up-down rows and left-right columns
        # divided the workers in colored groups(red,green) according to their location and whether they are odd or even
        # the communication part explained in detail can be found in report

        condition_1 = rank % (2 * c) <= c and rank % 2 == 1
        condition_2 = rank % (2 * c) > c and rank % 2 == 0
        condition_3 = rank % (2 * c) == 0

        # red colored ones first send the info and then wait to receive if they hit an edge condition they send empty
        # board piece in right size

        if condition_1 or condition_2 or condition_3:
        #red
            if not edge_down:
                comm.send(sub_board[worker_size_val - 1:worker_size_val, 0:], dest=down_neighbour)
            else:
                comm.send(empty_grid[worker_size_val - 1:worker_size_val, 0:], dest=down_neighbour)

            up_row = comm.recv(source=up_neighbour)

            if not edge_right:
                comm.send(sub_board[0:, worker_size_val - 1:worker_size_val], dest=right_neighbour)
            else:
                comm.send(empty_grid[0:, worker_size_val - 1:worker_size_val], dest=right_neighbour)

            left_column = comm.recv(source=left_neighbour)

            if not edge_up:
                comm.send(sub_board[0:1, 0:], dest=up_neighbour)
            else:
                comm.send(empty_grid[0:1, 0:], dest=up_neighbour)

            down_row = comm.recv(source=down_neighbour)

            if not edge_left:
                comm.send(sub_board[0:, 0:1], dest=left_neighbour)
            else:
                comm.send(empty_grid[0:, 0:1], dest=left_neighbour)

            right_column = comm.recv(source=right_neighbour)

        # green colored ones wait until they receive and then send if they hit an edge condition they send empty
        # board piece in right size
        else:
        #green
            up_row = comm.recv(source=up_neighbour)

            if not edge_down:
                comm.send(sub_board[worker_size_val - 1:worker_size_val, 0:], dest=down_neighbour)
            else:
                comm.send(empty_grid[worker_size_val - 1:worker_size_val, 0:], dest=down_neighbour)

            left_column = comm.recv(source=left_neighbour)

            if not edge_right:
                comm.send(sub_board[0:, worker_size_val - 1:worker_size_val], dest=right_neighbour)
            else:
                comm.send(empty_grid[0:, worker_size_val - 1:worker_size_val], dest=right_neighbour)

            down_row = comm.recv(source=down_neighbour)

            if not edge_up:
                comm.send(sub_board[0:1, 0:], dest=up_neighbour)
            else:
                comm.send(empty_grid[0:1, 0:], dest=up_neighbour)

            right_column = comm.recv(source=right_neighbour)

            if not edge_left:
                comm.send(sub_board[0:, 0:1], dest=left_neighbour)
            else:
                comm.send(empty_grid[0:, 0:1], dest=left_neighbour)

        # does communication for the diagonals
        # worker which has an odd rank sends the info and then waits to receive
        if rank % 2 == 1:

            if edge_up or edge_up_left:
                comm.send(float(empty_grid[0:1, 0:1]), dest=up_left_neighbour)
            else:
                comm.send(float(sub_board[0:1, 0:1]), dest=up_left_neighbour)

            down_right_corner = comm.recv(source=down_right_neighbour)

            if edge_up or edge_up_right:
                comm.send(float(empty_grid[0:1, worker_size_val - 1:worker_size_val]), dest=up_right_neighbour)
            else:
                comm.send(float(sub_board[0:1, worker_size_val - 1:worker_size_val]), dest=up_right_neighbour)

            down_left_corner = comm.recv(source=down_left_neighbour)

            if edge_down or edge_down_left:
                comm.send(float(empty_grid[worker_size_val - 1:worker_size_val, 0:1]), dest=down_left_neighbour)
            else:
                comm.send(float(sub_board[worker_size_val - 1:worker_size_val, 0:1]), dest=down_left_neighbour)

            up_right_corner = comm.recv(source=up_right_neighbour)

            if edge_down or edge_down_right:
                comm.send(float(empty_grid[worker_size_val - 1:worker_size_val, worker_size_val - 1:worker_size_val]),
                          dest=down_right_neighbour)
            else:
                comm.send(float(sub_board[worker_size_val - 1:worker_size_val, worker_size_val - 1:worker_size_val]),
                          dest=down_right_neighbour)

            up_left_corner = comm.recv(source=up_left_neighbour)

        # does communication for the diagonals
        # worker which has an even rank waits until it receives the info and then sends
        else:

            down_right_corner = comm.recv(source=down_right_neighbour)

            if edge_up or edge_up_left:
                comm.send(float(empty_grid[0:1, 0:1]), dest=up_left_neighbour)
            else:
                comm.send(float(sub_board[0:1, 0:1]), dest=up_left_neighbour)

            down_left_corner = comm.recv(source=down_left_neighbour)

            if edge_up or edge_up_right:
                comm.send(float(empty_grid[0:1, worker_size_val - 1:worker_size_val]), dest=up_right_neighbour)
            else:
                comm.send(float(sub_board[0:1, worker_size_val - 1:worker_size_val]), dest=up_right_neighbour)

            up_right_corner = comm.recv(source=up_right_neighbour)

            if edge_down or edge_down_left:
                comm.send(float(empty_grid[worker_size_val - 1:worker_size_val, 0:1]), dest=down_left_neighbour)
            else:
                comm.send(float(sub_board[worker_size_val - 1:worker_size_val, 0:1]), dest=down_left_neighbour)

            up_left_corner = comm.recv(source=up_left_neighbour)

            if edge_down or edge_down_right:
                comm.send(float(empty_grid[worker_size_val - 1:worker_size_val, worker_size_val - 1:worker_size_val]),
                          dest=down_right_neighbour)
            else:
                comm.send(float(sub_board[worker_size_val - 1:worker_size_val, worker_size_val - 1:worker_size_val]),
                          dest=down_right_neighbour)

        # compute remaining health of each tower
        # edge and corner elements computed according to their locations

        for i in range(0, worker_size_val):
            for j in range(0, worker_size_val):
                health = 0
                # character can be dot(0),circle(1) or plus(2)
                character = 0
                # put empty space
                if int(str(sub_board[i][j]).split('.')[0]) == 0:
                    health = 0
                    character = 0
                # put circle tower
                if int(str(sub_board[i][j]).split('.')[0]) == 1:
                    health = int(str(sub_board[i][j]).split('.')[1])
                    character = 1
                # put plus tower
                if int(str(sub_board[i][j]).split('.')[0]) == 2:
                    health = int(str(sub_board[i][j]).split('.')[1])
                    character = 2

                # one by one processor version when worker size value is 1

                if worker_size_val == 1:

                    if int(str(up_left_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[0][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[0][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(down_row[0][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_row[0][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(left_column[0][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(left_column[0][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(right_column[0][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(right_column[0][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(up_right_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_left_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_right_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # up left corner piece
                elif i == 0 and j == 0:

                    if int(str(up_left_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[0][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[0][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(up_row[0][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(left_column[0][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(left_column[0][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(left_column[1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i + 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # up right corner piece
                elif i == 0 and j == worker_size_val - 1:

                    if int(str(up_right_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[i][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[i][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(up_row[i][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(right_column[0][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(right_column[0][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(right_column[1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i + 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # down left corner piece
                elif i == worker_size_val - 1 and j == 0:
                    if int(str(down_left_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_row[0][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_row[0][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(down_row[0][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(left_column[worker_size_val - 1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(left_column[worker_size_val - 1][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(left_column[worker_size_val - 2][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1
                        
                # down right corner piece
                elif i == worker_size_val - 1 and j == worker_size_val - 1:
                    if int(str(down_right_corner).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_row[0][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_row[0][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(down_row[0][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(right_column[worker_size_val - 1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(right_column[worker_size_val - 1][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(right_column[worker_size_val - 2][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # up row excluding the corner pieces
                elif i == 0:
                    if int(str(up_row[0][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[0][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(up_row[0][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(up_row[0][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i + 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # down row excluding the corner pieces
                elif i == worker_size_val - 1:
                    if int(str(down_row[0][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_row[0][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(down_row[0][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(down_row[0][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # left column excluding the corner pieces
                elif j == 0:

                    if int(str(left_column[i][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(left_column[i][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(left_column[i - 1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(left_column[i + 1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # right column excluding the corner pieces
                elif j == worker_size_val - 1:

                    if int(str(right_column[i][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(right_column[i][0]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(right_column[i - 1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(right_column[i + 1][0]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # other middle pieces
                else:

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j + 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i + 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j + 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i - 1][j]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i][j - 1]).split(".")[0]) == 2 and character == 1:
                        health = health - 2

                    if int(str(sub_board[i - 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                    if int(str(sub_board[i + 1][j - 1]).split(".")[0]) == 1 and character == 2:
                        health = health - 1

                # change the tower health according to the rules stated
                if health <= 0:
                    new_board[i][j] = str(0.0)
                else:
                    if character == 2:
                        new_board[i][j] = "2." + str(health)
                    else:
                        new_board[i][j] = "1." + str(health)

        # all computed changes are made, save the new board into actual sub_board

        sub_board = new_board.copy()

    # after all the fight rounds, send the final board to the manager
    comm.send(sub_board, dest=0)
