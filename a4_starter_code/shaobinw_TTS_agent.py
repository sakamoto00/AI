
'''
Sean Wang
shaobinw@uw.edu
CSE 415 Assignment4
zobrist hashing and interesting utterance are implemented as extra credits
'''
from TTS_State import TTS_State
import time
#default settings
from random import randint

def get_ready(initial_state, input_k, what_side_i_play, opponent_moniker):
  global stateNow, mySide, oppo, myK
  global STATES_EXPENDED, EVALS_PERFORMED, DEPTH_REACHED, USE_ITERATIVE_DEEPENING, USE_CUSTOM_STATIC_EVAL_FUNCTION
  global zobristnum
  global myDictionary, S, P, piece
  global ZH_GET_NO_OK, ZH_GET_OK, ZH_PUT, ZH_GET
  global EARLY_GAME, STEP_TAKEN
  STEP_TAKEN = 0
  EARLY_GAME = True
  ZH_GET_OK = 0
  ZH_GET = 0
  ZH_GET_NO_OK = 0
  ZH_PUT = 0
  myDictionary = {}
  S = len(initial_state.board) * len(initial_state.board[0])
  P = 2
  zobristnum =[[0]*P for i in range(S)]
  for i in range(S):
    for j in range(P):
      zobristnum[i][j]=randint(0, 4294967296)
  USE_CUSTOM_STATIC_EVAL_FUNCTION = True
  USE_ITERATIVE_DEEPENING = True
  STATES_EXPENDED = 0
  EVALS_PERFORMED = 0
  DEPTH_REACHED = 0
  stateNow = initial_state
  mySide = what_side_i_play
  oppo = opponent_moniker
  myK = input_k
  return "ok"

def who_am_i():
  return ("My name is miracle-. \n Designed by Sean \"shaobinw\" Wang. \n I am greedy and get more aggressive along with the game process. ")

def moniker():
  return ("miracle-")

def take_turn(current_state, opponents_utterance, time_limit=10000):
  # Compute the new state for a move.
  # Start by copying the current state.
  #assert(current_state.whose_turn == mySide)
  global EARLY_GAME, STEP_TAKEN
  STEP_TAKEN += 2
  if (STEP_TAKEN >= (len(current_state.board)*len(current_state.board)/2)):
    EARLY_GAME = False
  start_time = time.time()
  new_state = MY_TTS_State(current_state.board)

  # Fix up whose turn it will be.
  who = current_state.whose_turn
  new_who = 'B'  
  if who=='B': new_who = 'W'  
  new_state.whose_turn = new_who

  #use iterative minimax algorithm to get the move
  minimax_result = iterative_minimax(current_state, start_time, time_limit)
  move = [minimax_result[2], minimax_result[3]]
  if(move == [-1, -1]): return [[False, current_state], "no more moves, ah oh."]
  new_state.board = minimax_result[0].board

  #generate an interesting utterance to show my agent's personality and 
  #some thoughts about the process of game playing
  advantage = new_state.static_eval()
  new_utterance = "I always try my best to get a longest line to win. "
  if ((minimax_result[1] == 99999 and mySide == "W") or (minimax_result[1] == -99999 and mySide == "B")):
    new_utterance += "Good Game, Well Played. "
  elif ((advantage > 0 and mySide == "W") or (advantage < 0 and mySide == "B")):
    new_utterance += "Take care, I am having some advantages. "
  elif ((advantage < 0 and mySide == "W") or (advantage > 0 and mySide == "B")):
    new_utterance += "Oh, you are actually doing very well. I will also try my best. "
  if ((minimax_result[1] > 0 and minimax_result[1] < 99999 and mySide == "W") or (minimax_result[1] < 0 and minimax_result[1] > -99999 and mySide == "B")):
    new_utterance += "According to my calculation, I am winning this game. "
  if ((minimax_result[1] < 0 and mySide == "W") or (minimax_result[1] > 0 and mySide == "B")):
    new_utterance += "But you still have chances. "
  #print(minimax_result[1])
  #return the move to the game master
  return [[move, new_state], new_utterance]

#iterative minimax function that repeatively run minimax but considers the time limit
def iterative_minimax(current_state, start_time, time_limit):
  i = 1
  while( (time.time() - start_time) < (time_limit / max(len(current_state.board)*len(current_state.board), len(current_state.board[0])*len(current_state.board[0]))*0.8)):
    STATES_EXPENDED = 0
    EVALS_PERFORMED = 0
    DEPTH_REACHED = 0
    minimax_result = minimax(current_state, i, current_state.whose_turn)
    if((current_state.whose_turn == "W" and minimax_result[1] == 99999) or (current_state.whose_turn == "B" and minimax_result[1] == -99999)):
      break
    i = i + 1
  DEPTH_REACHED = i - 1
  #print(DEPTH_REACHED)
  return minimax_result

#return all the available locations in the board b
def findAvailableLocations(b):
  results = []
  for i in range(len(b)):
      for j in range(len(b[0])):
        if b[i][j]==' ': results.append([i, j])
  return results;

#minimax function, return (bese_state, heuristic_eval_value)
def minimax(now_state, depth, which_side):
  global STATES_EXPENDED, EVALS_PERFORMED, DEPTH_REACHED, USE_ITERATIVE_DEEPENING, USE_CUSTOM_STATIC_EVAL_FUNCTION
  STATES_EXPENDED += 1
  now_state.__class__ = MY_TTS_State
  #base case for reursion
  if(depth == 0):
    EVALS_PERFORMED += 1
    return [now_state, now_state.static_eval(), -1, -1]
  #normal case, find every child
  new_locations = findAvailableLocations(now_state.board)
  if(new_locations == []):
    EVALS_PERFORMED += 1
    return [now_state, now_state.static_eval(), -1, -1]
  if (which_side == "W"):
    bestvalue = -100000
  else:
    bestvalue = 100000
  bestResult = [now_state, bestvalue, -1, -1]
  for i in range(len(new_locations)):
    if("W" == which_side):
      next_state = now_state.copy()
      next_state.board[new_locations[i][0]][new_locations[i][1]] = 'W'
      v = minimax(next_state, depth - 1, "B")
      if (v[1] > bestvalue):
        bestvalue = v[1]
        bestResult = [next_state ,v[1], new_locations[i][0], new_locations[i][1]]
    else:
      next_state = now_state.copy()
      next_state.board[new_locations[i][0]][new_locations[i][1]] = 'B'
      v = minimax(next_state, depth - 1, "W")
      if (v[1] < bestvalue):
        bestvalue = v[1]
        bestResult = [next_state, v[1], new_locations[i][0], new_locations[i][1]]
  return bestResult

def zhash(board):
  global zobristnum
  val = 0;
  for i in range(len(board)):
    for j in range(len(board[0])):
      piece = None
      if(board[i][j] == 'B'): piece = 0
      if(board[i][j] == 'W'): piece = 1
      if(piece != None):
        val ^= zobristnum[i * len(board[0]) + j][piece]
  return val

def _find_next_vacancy(b):
  for i in range(len(b)):
    for j in range(len(b[0])):
      if b[i][j]==' ': return (i,j)
  return False

#tryout function for testing and grading
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
  global STATES_EXPENDED, EVALS_PERFORMED, DEPTH_REACHED, USE_ITERATIVE_DEEPENING, USE_CUSTOM_STATIC_EVAL_FUNCTION, USE_ZOBRIST
  global ZH_PUT, ZH_GET, ZH_GET_OK, ZH_GET_NO_OK
  USE_CUSTOM_STATIC_EVAL_FUNCTION = use_custom_static_eval_function
  USE_ITERATIVE_DEEPENING = use_iterative_deepening
  USE_ZOBRIST = use_zobrist
  STATES_EXPENDED = 0
  EVALS_PERFORMED = 0
  DEPTH_REACHED = 0
  current_state_dynamic_val = minimax(current_state, max_ply, current_state.whose_turn)[1]
  current_state_static_val  = current_state.static_eval()
  if(use_iterative_deepening):
    v = iterative_minimax(current_state, time.time(), time_limit);
    max_depth_reached = DEPTH_REACHED
  else:
    max_depth_reached = max_ply
  n_states_expanded = STATES_EXPENDED
  n_static_evals_performed = EVALS_PERFORMED

  #not implemented
  n_ab_cutoffs = 0

  #z_hashing
  if(use_zobrist):
    n_zh_put_operations = ZH_PUT
    n_zh_get_operations = ZH_GET
    n_zh_successful_gets = ZH_GET_OK
    n_zh_unsuccessful_gets = ZH_GET_NO_OK
    zh_hash_value_of_current_state = zhash(current_state.board)
  else:
    n_zh_put_operations = 0
    n_zh_get_operations = 0
    n_zh_successful_gets = 0
    n_zh_unsuccessful_gets = 0
    zh_hash_value_of_current_state = 0

  #return result list
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
  return results

class MY_TTS_State(TTS_State):
  #a subclass of TTS_State
  global myK
  def static_eval(self):
    global myDictionary, ZH_GET, ZH_PUT, ZH_GET_OK, ZH_GET_NO_OK
    ZH_GET += 1
    if (zhash(self.board) in myDictionary):
      ZH_GET_OK += 1
      return myDictionary[zhash(self.board)]
    ZH_GET_NO_OK += 1
    ZH_PUT += 1
    if USE_CUSTOM_STATIC_EVAL_FUNCTION:
      result = self.custom_static_eval()
      myDictionary[zhash(self.board)] = result;
      return result
    else:
      result = self.basic_static_eval()
      myDictionary[zhash(self.board)] = result;
      return result

  def basic_static_eval(self):
    result = 0;
    rowNumber = len(self.board)
    colNumber = len(self.board[0])
    for i in range(rowNumber):
      for j in range(colNumber):
        if (self.board[i][j] != '-'):
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = (i + k) % rowNumber
            temp_j = (j + k) % colNumber
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(whiteCount == 2 and blackCount == 0 and not (blocked)):
            result = result + 1
          if(blackCount == 2 and whiteCount == 0 and not (blocked)):
            result = result - 1
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = (i + k) % rowNumber
            temp_j = j
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(whiteCount == 2 and blackCount == 0 and not (blocked)):
            result = result + 1
          if(blackCount == 2 and whiteCount == 0 and not (blocked)):
            result = result - 1
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = i % rowNumber
            temp_j = (j + k) % colNumber
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(whiteCount == 2 and blackCount == 0 and not (blocked)):
            result = result + 1
          if(blackCount == 2 and whiteCount == 0 and not (blocked)):
            result = result - 1
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = (i + k) % rowNumber
            temp_j = (j - k) % colNumber
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(whiteCount == 2 and blackCount == 0 and not (blocked)):
            result = result + 1
          if(blackCount == 2 and whiteCount == 0 and not (blocked)):
            result = result - 1
    return result;


  def custom_static_eval(self):
    global EARLY_GAME
    result = 0;
    rowNumber = len(self.board)
    colNumber = len(self.board[0])
    for i in range(rowNumber):
      for j in range(colNumber):
        if ((EARLY_GAME and self.board[i][j] == 'W' or self.board[i][j] == 'B') or (not EARLY_GAME and self.board[i][j] == 'B')):
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = (i + k) % rowNumber
            temp_j = (j + k) % colNumber
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(blackCount == 0 and not (blocked)):
            result = result + whiteCount*whiteCount*whiteCount
            if(whiteCount == myK):
              return 99999
            elif(whiteCount == myK - 1):
              return 9999
          if(whiteCount == 0 and not (blocked)):
            result = result - blackCount*blackCount*blackCount
            if(blackCount == myK):
              return -99999;
            elif(blackCount == myK - 1):
              return -9999
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = (i + k) % rowNumber
            temp_j = j % colNumber
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(blackCount == 0 and not (blocked)):
            result = result + whiteCount*whiteCount*whiteCount
            if(whiteCount == myK):
              return 99999
            elif(whiteCount == myK - 1):
              return 9999
          if(whiteCount == 0 and not (blocked)):
            result = result - blackCount*blackCount*blackCount
            if(blackCount == myK):
              return -99999
            elif(blackCount == myK - 1):
              return -9999
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = i % rowNumber
            temp_j = (j + k) % colNumber
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(blackCount == 0 and not (blocked)):
            result = result + whiteCount*whiteCount*whiteCount
            if(whiteCount == myK):
              return 99999
            elif(whiteCount == myK - 1):
              return 9999
          if(whiteCount == 0 and not (blocked)):
            result = result - blackCount*blackCount*blackCount
            if(blackCount == myK):
              return -99999
            elif(blackCount == myK - 1):
              return -9999
          whiteCount = 0
          blackCount = 0
          blocked = False
          for k in range(myK):
            temp_i = (i - k) % rowNumber
            temp_j = (j + k) % colNumber
            if(temp_i < 0):
              temp_i = (0 - temp_i) % rowNumber
            if(self.board[temp_i][temp_j] == 'W'):
              whiteCount = whiteCount + 1
            if(self.board[temp_i][temp_j] == 'B'):
              blackCount = blackCount + 1
            if(self.board[temp_i][temp_j] == '-'):
              blocked = True
          if(blackCount == 0 and not (blocked)):
            result = result + whiteCount*whiteCount*whiteCount
            if(whiteCount == myK):
              return 99999
            elif(whiteCount == myK - 1):
              return 9999
          if(whiteCount == 0 and not (blocked)):
            result = result - blackCount*blackCount*blackCount
            if(blackCount == myK):
              return -99999
            elif(blackCount == myK - 1):
              return -9999
    return result

if (__name__ == "__main__"):
  INITIAL_BOARD = \
           [[' ',' ',' ',' '],
            ['W',' ','B','B'],
            ['W',' ',' ','-'],
            [' ',' ','W',' ']]
  K = 3
  myGG = get_ready(TTS_State(INITIAL_BOARD, "B"), K, "B", "gger");
  result = tryout(TTS_State(INITIAL_BOARD, "B"), TTS_State(INITIAL_BOARD, "W"), 4, False, False, False, True, 1.0, True, True);
  print(result)
  print(USE_CUSTOM_STATIC_EVAL_FUNCTION)

