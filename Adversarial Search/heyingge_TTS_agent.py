'''PlayerSkeleton.py
A bare-bones agent that plays Toro-Tile Straight,
but rather poorly.

To create your own agent, make a copy of this file, using
the naming convention YourUWNetID_TTS_agent.py.

If you need to import additional custom modules, use
a similar naming convention... e.g.,
YourUWNetID_TTS_custom_static.py


'''

from TTS_State import TTS_State
from random import randint

USE_CUSTOM_STATIC_EVAL_FUNCTION = False
K = 3
I = 'W'
rows = 3
columns = 3

S = 64
P = 2
zobristnum = []
eval_dic = {}

class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        current_state = self.board
        CW2 = 0
        CB2 = 0
        for i in range(0, rows):
            for j in range(0, columns):
                current_square = current_state[i][j]
                if current_square != '-':
                    list_E = [current_square]
                    list_SE = [current_square]
                    list_S = [current_square]
                    list_SW = [current_square]
                    for k in (1, K):
                        list_E += current_state[i][(j + k) % columns] # E
                        list_SE += current_state[(i + k) % rows][(j + k) % columns] # SE
                        list_S += current_state[(i + k) % rows][j] # S
                        list_SW += current_state[(i + k) % rows][(j - k) % columns] # SW

                    result = self.static_eval_helper(list_E, 2)
                    if result == 0:
                        CW2 += 1
                    elif result == 1:
                        CB2 += 1

                    result = self.static_eval_helper(list_SE, 2)
                    if result == 0:
                        CW2 += 1
                    elif result == 1:
                        CB2 += 1

                    result = self.static_eval_helper(list_S, 2)
                    if result == 0:
                        CW2 += 1
                    elif result == 1:
                        CB2 += 1

                    result = self.static_eval_helper(list_SW, 2)
                    if result == 0:
                        CW2 += 1
                    elif result == 1:
                        CB2 += 1

        return CW2 - CB2

    def custom_static_eval(self):
        current_state = self.board
        CW = 0
        CB = 0

        for i in range(0, rows):
            for j in range(0, columns):
                coefficient = 100
                current_square = current_state[i][j]
                if current_square != '-':
                    list_E = [current_square]
                    list_SE = [current_square]
                    list_S = [current_square]
                    list_SW = [current_square]
                    for k in range(1, K):
                        list_E += current_state[i][(j + k) % columns]  # E
                        list_SE += current_state[(i + k) % rows][(j + k) % columns]  # SE
                        list_S += current_state[(i + k) % rows][j]  # S
                        list_SW += current_state[(i + k) % rows][(j - k) % columns]  # SW

                    for k in range(K - 1, 0, -1):
                        result = self.static_eval_helper(list_E, k)
                        if result == 0:
                            CW += coefficient
                        elif result == 1:
                            CB += coefficient

                        result = self.static_eval_helper(list_SE, k)
                        if result == 0:
                            CW += coefficient
                        elif result == 1:
                            CB += coefficient

                        result = self.static_eval_helper(list_S, k)
                        if result == 0:
                            CW += coefficient
                        elif result == 1:
                            CB += coefficient

                        result = self.static_eval_helper(list_SW, k)
                        if result == 0:
                            CW += coefficient
                        elif result == 1:
                            CB += coefficient
                        coefficient = coefficient / 10

        return CW - CB

    def static_eval_helper(self, list, k):
        W = 0
        B = 0
        for square in list:
            if square == '-':
                break
            if square == 'W':
                W += 1
            if square == 'B':
                B += 1
        if W == k and B == 0:
            return 0
        elif W == 0 and B == k:
            return 1
        else:
            return 2


def mini_max(current_state, ply):
        best_score = -99999
        best_move = False
        for new_state in find_successors(current_state):
            new_score = MIN(new_state, ply - 1)
            if new_score > best_score:
                best_score = new_score
                best_move = new_state.move
        return best_move


def MIN(current_state, ply):
    global eval_dic
    if _find_next_vacancy(current_state.board) == False:
        return 0
    elif win_tester(current_state):
        return 9999
    elif ply == 0:
        current_state.__class__ = MY_TTS_State
        hash = zhash(current_state.board)
        if hash in eval_dic:
            return eval_dic[hash]
        else:
            static_eval = current_state.custom_static_eval()
            eval_dic[hash] = static_eval
            return static_eval
    else:
        best_score = 99999
        for new_state in find_successors(current_state):
            best_score = min(best_score, MAX(new_state, ply - 1))
        return best_score


def MAX(current_state, ply):
    global eval_dic
    if _find_next_vacancy(current_state.board) == False:
        return 0
    elif win_tester(current_state):
        return -9999
    elif ply == 0:
        current_state.__class__ = MY_TTS_State
        hash = zhash(current_state.board)
        if hash in eval_dic:
            return eval_dic[hash]
        else:
            static_eval = current_state.custom_static_eval()
            eval_dic[hash] = static_eval
            return static_eval
    else:
        best_score = -99999
        for new_state in find_successors(current_state):
            best_score = max(best_score, MIN(new_state, ply - 1))
        return best_score

# return a list of states of possible successors
def find_successors(current_state):
    successors = []
    who = current_state.whose_turn
    new_who = 'B'
    if who == 'B': new_who = 'W'

    for i in range(0, rows):
        for j in range(0, columns):
            current_square = current_state.board[i][j]
            if current_square == ' ':
                new_state = MY_TTS_State(current_state.board, new_who)
                new_state.board[i][j] = who
                new_state.move = (i, j)
                successors.append(new_state)
    return successors

def win_tester(current_state):
    i = current_state.move[0]
    j = current_state.move[1]
    board = current_state.board
    who = board[i][j]

    win_N = 0
    for k in range(1, K):
        if board[(i - k) % rows][j] ==  who:   # N
            win_N += 1
        else: break

    win_NE = 0
    for k in range(1, K):
        if board[(i - k) % rows][(j + k) % columns] == who:  # NE
            win_NE += 1
        else: break

    win_E = 0
    for k in range(1, K):
        if board[i][(j + k) % columns] == who:  # E
            win_E += 1
        else: break

    win_SE = 0
    for k in range(1, K):
        if board[(i + k) % rows][(j + k) % columns] == who:  # SE
            win_SE += 1
        else: break

    win_S = 1
    for k in range(1, K):
        if board[(i + k) % rows][j] == who:  # S
            win_S += 1
        else: break

    win_SW = 1
    for k in range(1, K):
        if board[(i + k) % rows][(j - k) % columns] == who:  # SW
            win_SW += 1
        else: break

    win_W = 1
    for k in range(1, K):
        if board[i][(j - k) % columns] == who:  # W
            win_W += 1
        else: break

    win_NW = 1
    for k in range(1, K):
        if board[(i - k) % rows][(j - k) % columns] == who:  # NW
            win_NW += 1
        else: break

    return (win_N + win_S >= K) or (win_NE + win_SW >= K) or\
           (win_E + win_W >= K) or (win_SE + win_NW >= K)

def zhash(board):
    val = 0
    for i in range(0, rows):
        for j in range(0,columns):
            piece = None
            if board[i][j] == 'B':
                piece = 0
            if board[i][j] == 'W':
                piece = 1
            if piece is not None:
                val ^= zobristnum[i * columns + j][piece]
    return val

def take_turn(current_state, last_utterance, time_limit=10000):
    # Compute the new state for a move.
    # Start by copying the current state.
    new_state = MY_TTS_State(current_state.board)
    # Fix up whose turn it will be.
    who = current_state.whose_turn
    new_who = 'B'
    if who == 'B': new_who = 'W'
    new_state.whose_turn = new_who

    # Place a new tile
    location = mini_max(current_state,2)
    if location == False: return [[False, current_state], "I don't have any moves!"]
    new_state.board[location[0]][location[1]] = who

    # Construct a representation of the move that goes from the
    # currentState to the newState.
    move = location

    # Make up a new remark
    new_utterance = "I'll think harder in some future game. Here's my move"
    return [[move, new_state], new_utterance]


def _find_all_vacancies(b):
    list = []
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ': list.append((i, j))
    if len(list) == 0: return False
    else: return list


def _find_next_vacancy(b):
    for i in range(len(b)):
        for j in range(len(b[0])):
            if b[i][j] == ' ': return (i, j)
    return False


def moniker():
    return "GG"  # Return your agent's short nickname here.


def who_am_i():
    return """My name is MASTERMIND, created by Freddie He, UWNetID: heyingge.
              I consider myself to be better than the Player Dumbell."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like setting up Zobrist hashing, here.
    global K, I, rows, columns, S, zobristnum
    K = k
    I = who_i_play
    rows = len(initial_state.board)
    columns = len(initial_state.board[0])
    S = rows * columns
    zobristnum = [[0] * P for i in range(S)]

    for i in range(S):
        for j in range(P):
            zobristnum[i][j] = randint(0, 4294967296)
    return "OK"


# The following is a skeleton for the function called tryout,
# which should be a top-level function in each agent file.
# A tester or an autograder may do something like
# import ABC_TTS_agent as player
# and then it will be able to call tryout using something like this:
# tryout_results = player.tryout(**kwargs)

def tryout(
        game_initial_state=None,
        current_state=None,
        max_ply=2,
        use_iterative_deepening=False,
        use_row_major_move_ordering=False,
        alpha_beta=False,
        timed=False,
        time_limit=1.0,
        use_zobrist=False,
        use_custom_static_eval_function=False):
    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    current_state_dynamic_val = mini_max(current_state, max_ply)
    current_state_static_val = MY_TTS_State(current_state).basic_static_eval()
    n_states_expanded = 0
    n_static_evals_performed = 0
    max_depth_reached = 0

    # Those students doing the optional alpha-beta implementation,
    # return the correct number of cutoffs from your agent (either here or below).
    n_ab_cutoffs = 0

    # For those of you doing Zobrist hashing, have your
    # agent determine these values and include the correct
    # values here or overwrite the default values below.
    n_zh_put_operations = 0
    n_zh_get_operations = 0
    n_zh_successful_gets = 0
    n_zh_unsuccessful_gets = 0
    zh_hash_value_of_current_state = 0

    # STUDENTS: You may create the rest of the body of this function here.

    # Prepare to return the results...
    results = []
    results.append(current_state_dynamic_val)
    results.append(current_state_static_val)
    results.append(n_states_expanded)
    results.append(n_static_evals_performed)
    results.append(max_depth_reached)
    results.append(n_ab_cutoffs)
    results.append(n_zh_put_operations)
    results.append(n_zh_get_operations)
    results.append(n_zh_successful_gets)
    results.append(n_zh_unsuccessful_gets)
    results.append(zh_hash_value_of_current_state)
    # Actually return the list of all results...
    return (results)

