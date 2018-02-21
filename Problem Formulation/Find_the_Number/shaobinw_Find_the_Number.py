'''shaobinw_Farmer_Fox.py
by Sean Wang

Assignment 2, in CSE 415, Winter 2018

This file contains my problem formulation for the problem of
the Find the number problem
'''
#<METADATA>
QUIET_VERSION = "0.2"
PROBLEM_NAME = "Towers of Hanoi"
PROBLEM_VERSION = "0.2"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "7-JAN-2018"
PROBLEM_DESC=\
'''This formulation of the Towers of Hanoi problem uses generic
Python 3 constructs and has been tested with Python 3.6.
It is designed to work according to the QUIET2 tools interface.
'''
#</METADATA>

#<HELP_FUNCTIONS>
'''The function to determine the answer to the user's Ask input
return true if n-k is divisible by m, false elsewise'''
def is_n_minus_k_divisible_by_m(n, k, m):
   return ((n - k) % m) == 0

'''The function to determine if the user's input in Ask part is legal
Returns true if the input m is less than 1000 and meanwhile prime number, false elsewise
'''
def isPrimeUnderX(x, m):
   if m >= x:
      return False

   for i in range(2, m-1):
      if m % i == 0:
            return False
   if m<2:
      return False
   return True
#</HELP_FUNCTIONS>

#<COMMON_DATA>
MAX_NUMBER = 10
N_result = MAX_NUMBER  # Use default, but override if new value supplied
                 # by the user on the command line.
try:
   import sys
   arg2 = sys.argv[2]
   arg3 = sys.argv[3]
   assert int(arg2)<=int(arg3)
   MAX_NUMBER = int(arg3)
   N_result = int(arg2)
   print("Success")
except:
   print("Using default number of secrete number: "+str(N_result)+" and max number " + str(MAX_NUMBER))
   print(" (To use a specific number, enter it on the command line, e.g.,")
   print("python3 ../Int_Solv_Client.py _Find_the_Number " + str(N_result) + " " + str(MAX_NUMBER) + ")")
#</COMMON_DATA>

#<COMMON_CODE>
class State:
   def __init__(self, d, step, m_temp):
      self.d = d
      self.step = step
      self.m_temp = m_temp

   def __eq__(self, s2):
      for p in range(0, MAX_NUMBER+1):
         if self.d[p] != s2.d[p]: return False
      if self.m_temp != s2.m_temp: return False
      if self.step != s2.step: return False
      return True

   def __str__(self):
      if self.step == 1:
         temp_string = "None"
      else:
         temp_string = str(self.m_temp)
      txt = "CURRENT_STATE = question_phase: "+str(self.step - 1)+"\n"+\
            "last_m: "+temp_string+"\n"+\
            "possibilities: ["
      for p in range(0, MAX_NUMBER+1):
         if self.d[p]==1:
            txt += str(p) + " ,"
      return txt[:-2]+"]"

   def __hash__(self):
      return (self.__str__()).__hash__()

   def copy(self):
      news = State({}, self.step, self.m_temp)
      for p in range(0, MAX_NUMBER+1):
         news.d[p]=self.d[p]
         news.step = self.step
         news.m_temp = self.m_temp
      return news

   def can_move(self, x, ss):
      if ss!=self.step:
         return False
      if ss==1:
         return isPrimeUnderX(MAX_NUMBER, x)
      else:
         return x<self.m_temp

   def move(self, x, ss):
      if ss==1:
         news = self.copy()
         news.m_temp = x;
         news.step = news.step + 1
         return news
      else:
         news = self.copy()
         news.step = news.step - 1
         for p in range(0, MAX_NUMBER+1):
            if (is_n_minus_k_divisible_by_m(int(p), int(x), int(self.m_temp)) != (is_n_minus_k_divisible_by_m(int(N_result), int(x), int(self.m_temp)))):
               news.d[p] = 0
         return news;
def goal_test(s):
   temp = 0;
   for p in range(0, MAX_NUMBER+1):
      if s.d[p] == 1: temp=temp+1
      if temp>1: return False
   return True

def goal_message(s):
   return "Successful Guess!"

class Operator:
   def __init__(self, name, precond, state_transf):
      self.name = name
      self.precond = precond
      self.state_transf = state_transf

   def is_applicable(self, s):
      return self.precond(s)

   def apply(self, s):
      return self.state_transf(s)

#</COMMON_CODE>

#<INITIAL_STATE>
INITIAL_DICT = {}
for p in range(0, MAX_NUMBER+1):
   INITIAL_DICT[p] = 1
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT, 1, -1)
#</INITIAL_STATE>

#<OPERATORS>
OPERATORS = [Operator("Is N divisible by "+ str(m) +" after ...",
                         lambda s, m1 = m: s.can_move(m1, 1),
                         lambda s, m1 = m: s.move(m1, 1))
            for (m) in range(0, MAX_NUMBER+1)]

OPERATORS = OPERATORS + [Operator("... subtracting " + str(k) +" ?",
                         lambda s, k1 = k: s.can_move(k1, 2),
                         lambda s, k1 = k: s.move(k1, 2))
            for (k) in range(0, MAX_NUMBER+1)]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
