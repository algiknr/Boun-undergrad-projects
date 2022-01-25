# Aim is to find the next possible optimal move for a chess agent
# in depth of n_actions.

# CMPE_480 Artificial Intelligence Project_1
##################################################################
import sys


# gives the utility value according to the specific utility function stated in the description.
def get_utility_value(b):
    #  get_utility_value.counter gives how many times the utility function is called.
    get_utility_value.counter += 1

    pieces_dict = {'Q1': 0, 'Q2': 0, 'R1': 0, 'R2': 0, 'B1': 0, 'B2': 0}

    for row in range(board_len_square):
        for col in range(board_len_square):
            if b[row][col] == 'Q1':
                pieces_dict['Q1'] = pieces_dict['Q1'] + 1
            elif b[row][col] == 'Q2':
                pieces_dict['Q2'] = pieces_dict['Q2'] + 1
            elif b[row][col] == 'R1':
                pieces_dict['R1'] = pieces_dict['R1'] + 1
            elif b[row][col] == 'R2':
                pieces_dict['R2'] = pieces_dict['R2'] + 1
            elif b[row][col] == 'B1':
                pieces_dict['B1'] = pieces_dict['B1'] + 1
            elif b[row][col] == 'B2':
                pieces_dict['B2'] = pieces_dict['B2'] + 1
    utility_value = 9 * (pieces_dict['Q1'] - pieces_dict['Q2']) \
                    + 5 * (pieces_dict['R1'] - pieces_dict['R2']) \
                    + 3 * (pieces_dict['B1'] - pieces_dict['B2'])

    return utility_value


def actions_possible(state, max_or_min):
    list_of_actions_coordinates = []

    # directions = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']

    # Traversing all the cells in order to get possible actions according to current agent
    for i in range(board_len_square):
        for j in range(board_len_square):
            if state[i][j] != "X" and state[i][j] != "x":
                if (max_or_min == 'max' and int(state[i][j][1]) == 1) or (
                        max_or_min == 'min' and int(state[i][j][1]) == 2):

                    if state[i][j][0] != 'B':
                        if i != 0:
                            list_of_actions_coordinates.append(["N", i, j])
                    if state[i][j][0] != 'R':
                        if i != 0 and j != board_len_square - 1:
                            list_of_actions_coordinates.append(["NE", i, j])
                    if state[i][j][0] != 'B':
                        if j != board_len_square - 1:
                            list_of_actions_coordinates.append(["E", i, j])
                    if state[i][j][0] != 'R':
                        if i != board_len_square - 1 and j != board_len_square - 1:
                            list_of_actions_coordinates.append(["SE", i, j])
                    if state[i][j][0] != 'B':
                        if i != board_len_square - 1:
                            list_of_actions_coordinates.append(["S", i, j])
                    if state[i][j][0] != 'R':
                        if i != board_len_square - 1 and j != 0:
                            list_of_actions_coordinates.append(["SW", i, j])
                    if state[i][j][0] != 'B':
                        if j != 0:
                            list_of_actions_coordinates.append(["W", i, j])
                    if state[i][j][0] != 'R':
                        if i != 0 and j != 0:
                            list_of_actions_coordinates.append(["NW", i, j])

    return list_of_actions_coordinates


def evaluate_new_board(action_coordinates_list, state):
    new_state = [[state[i][j] for j in range(len(state[0]))] for i in range(len(state))]  # deep copy

    action = action_coordinates_list[0]
    row = action_coordinates_list[1]
    column = action_coordinates_list[2]
    temp_r_c = [row, column]

    if action == "N":

        while state[row - 1][column] == "X" or state[row - 1][column] == "x":
            row = row - 1
            if row == 0:
                row = 1
                break
        new_state[row - 1][column] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "x"

    elif action == "NE":
        while state[row - 1][column + 1] == "X" or state[row - 1][column + 1] == "x":
            row = row - 1
            column = column + 1
            if row == 0 or column == board_len_square - 1:
                if row == 0 and column == board_len_square - 1:
                    row = 1
                    column = board_len_square - 2
                elif column == board_len_square - 1 and row != 0:
                    row = row + 1
                    column = board_len_square - 2
                elif column != board_len_square - 1 and row == 0:
                    row = 1
                    column = column - 1

                break
        new_state[row - 1][column + 1] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "x"

    elif action == "E":
        while state[row][column + 1] == "X" or state[row][column + 1] == "x":
            column = column + 1
            if column == board_len_square - 1:
                column = board_len_square - 2
                break
        new_state[row][column + 1] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "X"

    elif action == "SE":
        while state[row + 1][column + 1] == "X" or state[row + 1][column + 1] == "x":
            row = row + 1
            column = column + 1
            if row == board_len_square - 1 or column == board_len_square - 1:
                if row == board_len_square - 1 and column == board_len_square - 1:
                    row = board_len_square - 2
                    column = board_len_square - 2
                elif column == board_len_square - 1 and row != board_len_square - 1:
                    column = board_len_square - 2
                    row = row - 1
                elif column != board_len_square - 1 and row == board_len_square - 1:
                    row = board_len_square - 2
                    column = column - 1

                break

        new_state[row + 1][column + 1] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "x"
    elif action == "S":

        while state[row + 1][column] == "X" or state[row + 1][column] == "x":
            row = row + 1
            if row == board_len_square - 1:
                row = board_len_square - 2
                break
        new_state[row + 1][column] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "x"

    elif action == "SW":

        while state[row + 1][column - 1] == "X" or state[row + 1][column - 1] == "x":
            row = row + 1
            column = column - 1
            if row == board_len_square - 1 or column == 0:
                if row == board_len_square - 1 and column == 0:
                    row = board_len_square - 2
                    column = 1
                elif row == board_len_square - 1 and column != 0:
                    row = board_len_square - 2
                    column = column + 1
                elif row != board_len_square - 1 and column == 0:
                    row = row - 1
                    column = 1
                break
        new_state[row + 1][column - 1] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "x"

    elif action == "W":

        while state[row][column - 1] == "X" or state[row][column - 1] == "x":
            column = column - 1
            if column == 0:
                column = 1
                break
        new_state[row][column - 1] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "x"


    elif action == "NW":

        while state[row - 1][column - 1] == "X" or state[row - 1][column - 1] == "x":
            row = row - 1
            column = column - 1
            if row <= 0 or column <= 0:
                if row == 0 and column == 0:
                    row = 1
                    column = 1
                elif column != 0 and row == 0:
                    row = 1
                    column = column + 1
                elif column == 0 and row != 0:
                    row = row + 1
                    column = 1

                break
        new_state[row - 1][column - 1] = state[temp_r_c[0]][temp_r_c[1]]
        new_state[temp_r_c[0]][temp_r_c[1]] = "x"

    return new_state


def rand_value(state, counter, n_actions, search_type, alpha=None, beta=None):
    actions = actions_possible(state, "min")
    actionAndValues = []
    for action in actions:
        actionValue_after = max_value(evaluate_new_board(action, state), counter + 1, n_actions, search_type)
        actionAndValues.append([action, actionValue_after])

    values = []
    for actionAndValues in actionAndValues:
        values.append(actionAndValues[1])
    return sum(values) / len(values)  # returns avg value


def min_value(state, counter, n_actions, search_type, alpha=None, beta=None):
    actions = actions_possible(state, 'min')
    actionAndValues = []

    if search_type == 'minimax':
        for action in actions:
            actionValue_after = max_value(evaluate_new_board(action, state), counter + 1, n_actions, search_type)
            actionAndValues.append([action, actionValue_after])

    elif search_type == 'alpha_beta_pruning':
        ab = 1000000
        for action in actions:
            ab = min(ab, max_value(evaluate_new_board(action, state), counter + 1, n_actions, search_type, alpha, beta))
            if ab <= alpha:
                return ab
            beta = min(beta, ab)
        return ab

    actionAndValues.sort(key=lambda x: x[1])

    return actionAndValues[0][1]  # returns minimum value


def max_value(state, counter, n_actions, search_type, alpha=None, beta=None):
    if counter == n_actions + 1:
        return get_utility_value(state)

    actions = actions_possible(state, 'max')
    actionAndValues = []

    if search_type == "minimax":
        for action in actions:
            actionValue_after = min_value(evaluate_new_board(action, state), counter, n_actions, search_type)
            actionAndValues.append([action, actionValue_after])
    elif search_type == "minimax_rand":
        for action in actions:
            actionValue_after = rand_value(evaluate_new_board(action, state), counter, n_actions, search_type)
            actionAndValues.append([action, actionValue_after])
    elif search_type == 'alpha_beta_pruning':
        ab = -1000000
        for action in actions:
            ab = max(ab, min_value(evaluate_new_board(action, state), counter, n_actions, search_type, alpha, beta))
            if ab >= beta:
                return ab
            alpha = max(alpha, ab)
        return ab

    actionAndValues.sort(key=lambda x: x[1])
    return actionAndValues[-1][1]  # returns max value


def minimax_decision(state, n_actions, search_type):
    actions = actions_possible(state, 'max')
    actionAndValues = []

    if search_type == 'minimax':
        for action in actions:
            actionValue_after = min_value(evaluate_new_board(action, state), 1, n_actions, search_type)
            actionAndValues.append([action, actionValue_after])
    elif search_type == 'minimax_rand':
        for action in actions:
            actionValue_after = rand_value(evaluate_new_board(action, state), 1, n_actions, search_type)
            actionAndValues.append([action, actionValue_after])
    elif search_type == 'alpha_beta_pruning':
        alpha = -1000000
        beta = 1000000
        ab = -1000000
        for action in actions:
            ab = max(ab, min_value(evaluate_new_board(action, state), 1, n_actions, search_type, alpha, beta))
            alpha = max(alpha, ab)
            actionAndValues.append([action, ab])

    max_value = -1000000
    OutputAction = ""

    for action_value_pair in actionAndValues:
        if action_value_pair[1] > max_value:
            max_value = action_value_pair[1]
            OutputAction = action_value_pair[0]

    action = "Move {} {}".format(state[OutputAction[1]][OutputAction[2]][0], OutputAction[0])
    return action, "{:.2f}".format(max_value), get_utility_value.counter


# Creating the board from given file
def get_array(filename):
    arr = []

    f = open(filename, "r")
    size = int(f.readline().split("\n")[0].split()[0])
    for _ in range(size):
        arr.append(f.readline().split("\n")[0].split())
    f.close()

    return size, arr


if __name__ == '__main__':
    search_type, init_file, n_actions = sys.argv[1:]
    n_actions = int(n_actions)

    # construct arr_init from init_file
    _, arr_init = get_array(init_file)

    global board_len_square
    board_len_square = len(arr_init)

    get_utility_value.counter = 0

    action, value, n_util_calls = minimax_decision(arr_init, n_actions, search_type)

    print("Action: {}".format(action))
    print("Value: {}".format(value))
    print("Util calls: {}".format(n_util_calls))

    # print('ending')
