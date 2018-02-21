''' shaobinw_IDDFS.py
Iterative IDDFS Search of a problem space.
 Version 0.1, January 20, 2018.
 Steve Tanimoto, Univ. of Washington.
 Paul G. Allen School of Computer Science and Engineering

 Usage:
 python3 shaobinw_IDDFS.py TowersOfHanoi
# The numbered STEP comments in the function IterativeDFS correspond
 to the algorithm steps for iterative IDDF as presented
 in Slide 8 of the "Basic Search Algorithms" lecture.
'''

import sys

if sys.argv==[''] or len(sys.argv)<2:
#  import EightPuzzle as Problem
  import TowersOfHanoi as Problem
else:
  import importlib
  Problem = importlib.import_module(sys.argv[1])

print("\nWelcome to BreadthFS")
COUNT = None
BACKLINKS = {}

def runDFS():
  initial_state = Problem.CREATE_INITIAL_STATE()
  print("Initial State:")
  print(initial_state)
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH
  COUNT = 0
  BACKLINKS = {}
  MAX_OPEN_LENGTH = 0
  IDDFS(initial_state)
  print(str(COUNT)+" states expanded.")
  print('MAX_OPEN_LENGTH = '+str(MAX_OPEN_LENGTH))

def IDDFS(initial_state):
  global COUNT, BACKLINKS, MAX_OPEN_LENGTH
  DEPTH = 0
  CLOSED = []

  while True:
    OPEN = [initial_state]
    BACKLINKS[initial_state] = None
    CLOSED = []
    DEPTH += 1
    depthNow = 1
    ##operate DFS w/ DEPTH limitation
    while OPEN != []:
      report(OPEN, CLOSED, COUNT)
      if len(OPEN)>MAX_OPEN_LENGTH: MAX_OPEN_LENGTH = len(OPEN)

      S = OPEN.pop(0)
      CLOSED.append(S)
      depthNow = len(backtrace(S)) - 1

      if Problem.GOAL_TEST(S):
        print(Problem.GOAL_MESSAGE_FUNCTION(S))
        path = backtrace(S)
        print("Solution path: ")
        for s in path:
          print(s)
        print('Length of solution path found: '+str(len(path)-1)+' edges')
        return
      COUNT += 1

      L = []
      for op in Problem.OPERATORS:
        if op.precond(S) and depthNow < DEPTH:
          new_state = op.state_transf(S)
          if not (new_state in CLOSED):
            L.append(new_state)
            if (not (new_state in BACKLINKS) or
              (len(backtrace(S)) < len(backtrace(BACKLINKS[new_state])))):
              BACKLINKS[new_state] = S

      for s2 in L:
        for i in range(len(OPEN)):
          if (s2 == OPEN[i]):
            del OPEN[i]; break

      OPEN = L + OPEN
      print_state_list("OPEN", OPEN)


def print_state_list(name, lst):
  if lst == []: return
  print(name+" is now: ",end='')
  for s in lst[:-1]:
    print(str(s),end=', ')
  print(str(lst[-1]))

def backtrace(S):
  global BACKLINKS
  path = []
  while S:
    path.append(S)
    S = BACKLINKS[S]
  path.reverse()
  return path    
  
def report(open, closed, count):
  print("len(OPEN)="+str(len(open)), end='; ')
  print("len(CLOSED)="+str(len(closed)), end='; ')
  print("COUNT = "+str(count))

if __name__=='__main__':
  runDFS()

