'''shaobinw_Farmer_Fox.py
by Sean Wang

Assignment 2, in CSE 415, Winter 2018

This file contains my problem formulation for the problem of
the Farmer, Fox, Chicken, and Grain.
'''
#<METADATA>
QUIET_VERSION = "0.1"
PROBLEM_NAME = "_Farmer_Fox_etc"
PROBLEM_VERSION = "0.1"
PROBLEM_AUTHORS = ['S. Tanimoto']
PROBLEM_CREATION_DATE = "7-JAN-2018"
PROBLEM_DESC=\
'''This problem is so cool to solve the Farmer Fox Chicken and Grain
Problem with simple codes using Python 3 constructs. Wow!
'''
#</METADATA>

#<COMMON_CODE>
class State:
   def __init__(self, d):
      self.d = d

   def __eq__(self, s2):
      for p in ['farmer', 'fox', 'chicken', 'grain']:
         if self.d[p] != s2.d[p]: return False
      return True

   def __str__(self):
      txt = "["
      for p in ['farmer', 'fox', 'chicken', 'grain']:
         txt += str(self.d[p]) + " ,"
      return txt[:-2]+"]"

   def __hash__(self):
      return (self.__str__()).__hash__()

   def copy(self):
      news = State({'farmer':self.d['farmer'],
                    'fox':self.d['fox'], 
                    'chicken':self.d['chicken'], 
                    'grain':self.d['grain']})
      return news

   def can_move(self, animal):
      try:
         pf=self.d['farmer'] # the position of farmer
         if(animal!='none'):
            if(pf!=self.d[animal]):
               return False
         if (animal == 'fox') or (animal=='none'):
            if(pf == self.d['chicken']) and (pf == self.d['grain']):
               return False
         if (animal == 'grain') or (animal=='none'):
            if(pf == self.d['chicken']) and (pf == self.d['fox']):
               return False
         return True
      except (Exception) as e:
         print(e)

   def move(self, animal):
      news = self.copy() # start with a deep copy.
      if (animal != 'none'):
         news.d[animal] = self.d[animal] * -1
      news.d['farmer'] = self.d['farmer'] * -1
      return news

def goal_test(s):
   for p in ['farmer', 'fox', 'chicken', 'grain']:
      if s.d[p] == -1: return False
   return True

def goal_message(s):
   return "You are aMaZing!!!!! OMG!!!!"

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
INITIAL_DICT = {'farmer':-1, 'fox':-1, 'chicken':-1, 'grain':-1}
CREATE_INITIAL_STATE = lambda: State(INITIAL_DICT)
#</INITIAL_STATE>

#<OPERATORS> 
OPERATORS = [Operator("Move the farmer with " + p,
                       lambda s, p1=p: s.can_move(p1),
                       lambda s, p1=p: s.move(p1))
             for (p) in ['fox', 'chicken', 'grain', 'none']]
#</OPERATORS>

#<GOAL_TEST> (optional)
GOAL_TEST = lambda s: goal_test(s)
#</GOAL_TEST>

#<GOAL_MESSAGE_FUNCTION> (optional)
GOAL_MESSAGE_FUNCTION = lambda s: goal_message(s)
#</GOAL_MESSAGE_FUNCTION>
