'''PlayerSkeleton.py
wanjia09_TTS_agent.py
'''
import time
from TTS_State import *
#from TTS_win_tester import TTS_win_tester

USE_CUSTOM_STATIC_EVAL_FUNCTION = False

class MY_TTS_State(TTS_State):
    def static_eval(self):
        if USE_CUSTOM_STATIC_EVAL_FUNCTION:
            return self.custom_static_eval()
        else:
            return self.basic_static_eval()

    def basic_static_eval(self):
        '''start with a deep copy of the current board'''
        current_state = self.copy()
        borad_row_count = len(current_state.board)
        board_column_count = len(current_state.board[0])
        white_count = 0
        black_count = 0
        current_board = current_state.board
        for i in range(0, borad_row_count):
            for j in range(0, borad_row_count):
                current_piece = current_board[i][j]
                # direction: East
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[i][(j + k) % borad_row_count] == 'W'):
                        w_count+= 1
                    elif(current_board[i][(j + k) % borad_row_count] == 'B'):
                        b_count += 1
                    string_rep += current_board[i][(j + k) % borad_row_count]
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count += 1
                    #print('white_count + 1: ', (i, j), ' dir:', 'E')
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count += 1
                    #print('black_count + 1: ', (i, j), ' dir:', 'E')

                #direction South
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[(i + k) % board_column_count][j] == 'W'):
                        w_count+= 1
                    elif(current_board[(i + k) % board_column_count][j] == 'B'):
                        b_count += 1
                    string_rep += current_board[(i + k) % board_column_count][j]
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count += 1
                    #print('white_count + 1: ', (i, j), ' dir:', 'S')
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count += 1
                    #print('black_count + 1: ', (i, j), ' dir:', 'S')

                # direction SE
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[(i + k) % board_column_count][(j + k) % borad_row_count] == 'W'):
                        w_count+= 1
                    elif(current_board[(i + k) % board_column_count][(j + k) % borad_row_count] == 'B'):
                        b_count += 1
                    string_rep += current_board[(i + k) % board_column_count][(j + k) % borad_row_count]
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count += 1
                    #print(k)
                    #print('white_count + 1: ', (i, j), ' dir:', 'SE')
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count += 1
                    #print('black_count + 1: ', (i, j), ' dir:', 'SE')

                # direction NE
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[(i - k) % board_column_count][(j + k) % borad_row_count] == 'W'):
                        w_count+= 1
                    elif(current_board[(i - k) % board_column_count][(j + k) % borad_row_count] == 'B'):
                        b_count += 1
                    string_rep += current_board[(i - k) % board_column_count][(j + k) % borad_row_count]
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count += 1
                    #print('white_count + 1: ', (i, j), ' dir:', 'NE')
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count += 1
                    #print('black_count + 1: ', (i, j), ' dir:', 'NE')
        return white_count - black_count

    def custom_static_eval(self):
        # raise Exception("custom_static_eval not yet implemented.")
        current_state = self.copy()
        borad_row_count = len(current_state.board)
        board_column_count = len(current_state.board[0])
        white_count_1 = 0
        black_count_1 = 0
        white_count_2 = 0
        black_count_2 = 0
        white_count_3 = 0
        black_count_3 = 0
        current_board = current_state.board
        for i in range(0, borad_row_count):
            for j in range(0, borad_row_count):
                current_piece = current_board[i][j]
                # direction: East
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[i][(j + k) % borad_row_count] == 'W'):
                        w_count+= 1
                    elif(current_board[i][(j + k) % borad_row_count] == 'B'):
                        b_count += 1
                    string_rep += current_board[i][(j + k) % borad_row_count]

                if '-' not in string_rep and w_count == 1 and b_count == 0:
                    white_count_1 += 1
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count_2 += 1
                if '-' not in string_rep and w_count == 3 and b_count == 0:
                    white_count_3 += 1
                if '-' not in string_rep and b_count == 1 and w_count == 0:
                    black_count_1 += 1
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count_2 += 1
                if '-' not in string_rep and b_count == 3 and w_count == 0:
                    black_count_3 += 1

                #direction South
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[(i + k) % board_column_count][j] == 'W'):
                        w_count+= 1
                    elif(current_board[(i + k) % board_column_count][j] == 'B'):
                        b_count += 1
                    string_rep += current_board[(i + k) % board_column_count][j]
                if '-' not in string_rep and w_count == 1 and b_count == 0:
                    white_count_1 += 1
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count_2 += 1
                if '-' not in string_rep and w_count == 3 and b_count == 0:
                    white_count_3 += 1
                if '-' not in string_rep and b_count == 1 and w_count == 0:
                    black_count_1 += 1
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count_2 += 1
                if '-' not in string_rep and b_count == 3 and w_count == 0:
                    black_count_3 += 1

                # direction SE
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[(i + k) % board_column_count][(j + k) % borad_row_count] == 'W'):
                        w_count+= 1
                    elif(current_board[(i + k) % board_column_count][(j + k) % borad_row_count] == 'B'):
                        b_count += 1
                    string_rep += current_board[(i + k) % board_column_count][(j + k) % borad_row_count]
                if '-' not in string_rep and w_count == 1 and b_count == 0:
                    white_count_1 += 1
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count_2 += 1
                if '-' not in string_rep and w_count == 3 and b_count == 0:
                    white_count_3 += 1
                if '-' not in string_rep and b_count == 1 and w_count == 0:
                    black_count_1 += 1
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count_2 += 1
                if '-' not in string_rep and b_count == 3 and w_count == 0:
                    black_count_3 += 1

                # direction NE
                string_rep = ''
                b_count = 0
                w_count = 0
                for k in range(0, K):
                    if (current_board[(i - k) % board_column_count][(j + k) % borad_row_count] == 'W'):
                        w_count+= 1
                    elif(current_board[(i - k) % board_column_count][(j + k) % borad_row_count] == 'B'):
                        b_count += 1
                    string_rep += current_board[(i - k) % board_column_count][(j + k) % borad_row_count]
                if '-' not in string_rep and w_count == 1 and b_count == 0:
                    white_count_1 += 1
                if '-' not in string_rep and w_count == 2 and b_count == 0:
                    white_count_2 += 1
                if '-' not in string_rep and w_count == 3 and b_count == 0:
                    white_count_3 += 1
                if '-' not in string_rep and b_count == 1 and w_count == 0:
                    black_count_1 += 1
                if '-' not in string_rep and b_count == 2 and w_count == 0:
                    black_count_2 += 1
                if '-' not in string_rep and b_count == 3 and w_count == 0:
                    black_count_3 += 1

        return 300 * (white_count_3 - black_count_3) + 10 * (white_count_2 - black_count_2) + (white_count_1 - black_count_1)
     
def take_turn(current_state, last_utterance, time_limit=10000):
    global max_ply, use_iterative_deepening
    new_state = MY_TTS_State(current_state.board)
    who = current_state.whose_turn
    use_iterative_deepening = False
    
    if use_iterative_deepening == True:
        start_time = time.time()
        time_lapsed = 0
        depth_attempted = 0
        new_utterance = 'I think in limited time! Woohoo!'
        move = (0, 0)
        while time_lapsed < time_limit:
            (value , move) = mini_max_helper(new_state, depth_attempted, who)
            depth_attempted += 1
            time_lapsed = time.time() - start_time
        new_state.board[move[0]][move[1]] = who
        new_state.whose_turn = other(who)
        return [[move, new_state], new_utterance]

    else:
        (value , move) = mini_max_helper(new_state, 2, who)
        new_state.board[move[0]][move[1]] = who
        new_state.whose_turn = other(who)
        new_utterance = 'I am 2 steps ahead of you.'
        return [[move, new_state], new_utterance]

def mini_max_helper(state, depth, player):
    #new_utterance = 'Well I need to say something.'
    #start with a deep copy 
    state_in_use = MY_TTS_State(state.board)
    if depth == 0:
        return state_in_use.custom_static_eval(), (0,0)
    if player == 'W':
        provisional = -100000
    else:
        provisional = 100000
    best_move = (0, 0)
    for i in range(len(state_in_use.board)):
        for j in range(len(state_in_use.board[0])):
            if state_in_use.board[i][j] == ' ':
                move = (i, j)
                current_board = state_in_use.copy()
                current_board.board[i][j] = player
                #current_board.whose_turn = other(player)
                (new_value, last_move) = mini_max_helper(current_board,depth -1, other(player))
                if ((player == 'W' and new_value > provisional) or (player == 'B' and new_value < provisional)):
                    provisional = new_value
                    best_move = move
                # state_in_use.board[i][j] = ' '
    return provisional, best_move

def other(player):
    if player == 'W':
        return 'B'
    if player == 'B':
        return 'W'    
    
def moniker():
    return "Alex" 

def who_am_i():
    return """My name is Alex, created by Wanjia Tang. I consider myself to be an android that speaks."""

def get_ready(initial_state, k, who_i_play, player2Nickname):
    # do any prep, like setting up Zobrist hashing, here.
    global max_ply, borad_row_count, board_column_count, K,timed, use_iterative_deepening
    timed = True
    max_ply = 2
    K = k
    borad_row_count = len(initial_state.board)
    board_column_count = len(initial_state.board[0])
    return "OK"

def _find_next_vacancy(b):
    for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': return (i,j)
    return False

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
       use_iterative_deepening = False,
       use_row_major_move_ordering = False,
       alpha_beta=False, 
       timed=False, 
       time_limit=1.0,
       use_zobrist=False,
       use_custom_static_eval_function=False):

    # All students, add code to replace these default
    # values with correct values from your agent (either here or below).
    global iterative_deepening
    iterative_deepening = use_iterative_deepening

    current_state_dynamic_val = -1000.0
    current_state_static_val  = -1000.0
    n_states_expanded = 0
    n_static_evals_performed = 0
    max_depth_reached = 0
    global USE_CUSTOM_STATIC_EVAL_FUNCTION
    USE_CUSTOM_STATIC_EVAL_FUNCTION = True 
    get_ready(INITIAL_STATE, K, 'W', 'Bobby')
    take_turn(INITIAL_STATE, 'What?')

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
    return(results)


if __name__ == "__main__":
    state = MY_TTS_State(INITIAL_BOARD)
    print(state.basic_static_eval())
    tryout(
       game_initial_state=None,
       current_state=None,
       max_ply=2,
       use_iterative_deepening = False,
       use_row_major_move_ordering = False,
       alpha_beta=False, 
       timed=False, 
       time_limit=1.0,
       use_zobrist=False,
       use_custom_static_eval_function=False)
 