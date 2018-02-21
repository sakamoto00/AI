'''YourUWNetID_Q_Learn.py

Rename this file using your own UWNetID, and rename it where it is imported
in TOH_MDP.py 
Implement Q-Learning in this file by completing the implementations
of the functions whose stubs are present.
Add or change code wherever you see #*** ADD OR CHANGE CODE HERE ***

This is part of the UW Intro to AI Starter Code for Reinforcement Learning.

'''
import random
# Edit the returned name to ensure you get credit for the assignment.
def student_name():
#*** ADD OR CHANGE CODE HERE ***
   return "Wang, Sean" # For an autograder.

STATES=None; ACTIONS=None; UQV_callback=None; Q_VALUES=None
is_valid_goal_state=None; Terminal_state = None
USE_EXPLORATION_FUNCTION = None; EPSILON_NOW = None
INITIAL_STATE = None
def setup(states, actions, q_vals_dict, update_q_value_callback,\
    goal_test, terminal, use_exp_fn=False):
    '''This method is called by the GUI the first time a Q_Learning
    menu item is selected. It may be called again after the user has
    restarted from the File menu.
    Q_VALUES starts out with all Q-values at 0.0 and a separate key
    for each (s, a) pair.'''
    global STATES, ACTIONS, UQV_callback, Q_VALUES, is_valid_goal_state
    global use_exploration_function, Terminal_state, EPSILON_NOW, ALPHA_NOW
    STATES = states
    ACTIONS = actions
    Q_VALUES = q_vals_dict
    UQV_callback = update_q_value_callback
    is_valid_goal_state = goal_test
    Terminal_state = terminal
    USE_EXPLORATION_FUNCTION = use_exp_fn
    EPSILON_NOW = 999
    EPSILON_NOW = 999
    extract_policy(STATES, ACTIONS)
    if USE_EXPLORATION_FUNCTION:
#*** ADD OR CHANGE CODE HERE ***
         # Change this if you implement an exploration function:
         print("You have not implemented an exploration function")

PREVIOUS_STATE = None
LAST_ACTION = None
def set_starting_state(s):
    '''This is called by the GUI when a new episode starts.
    Do not change this function.'''
    global INITIAL_STATE, PREVIOUS_STATE
    print("In Q_Learn, setting the starting state to "+str(s))
    INITIAL_STATE = s
    PREVIOUS_STATE = s

ALPHA = 0.5
CUSTOM_ALPHA = False
EPSILON = 0.5
CUSTOM_EPSILON = False
GAMMA = 0.9
def set_learning_parameters(alpha, epsilon, gamma):
    ''' Called by the system. Do not change this function.'''
    global ALPHA, EPSILON, CUSTOM_ALPHA, CUSTOM_EPSILON, GAMMA
    ALPHA = alpha
    EPSILON = epsilon
    GAMMA = gamma
    if alpha < 0: CUSTOM_ALPHA = True
    else: CUSTOM_ALPHA = False
    if epsilon < 0: CUSTOM_EPSILON = True
    else: CUSTOM_EPSILON = False

def update_Q_value(previous_state, previous_action, new_value):
    '''Whenever your code changes a value in Q_VALUES, it should
    also call this method, so the changes can be reflected in the
    display.
    Do not change this function.'''
    UQV_callback(previous_state, previous_action, new_value)

def handle_transition(action, new_state, r):
    '''When the user drives the agent, the system will call this function,
    so that you can handle the learning that should take place on this
    transition.'''
    global PREVIOUS_STATE, Q_VALUES, GAMMA, ALPHA, ACTIONS, STATES
    max_new_q = -999
    for a in ACTIONS:
        max_new_q = max(max_new_q, Q_VALUES[(new_state, a)])
    sample = r + GAMMA * max_new_q 
    new_reward = (1 - ALPHA) * Q_VALUES[(PREVIOUS_STATE, action)] + (ALPHA * sample)
    
    Q_VALUES[(PREVIOUS_STATE, action)] = new_reward
    # You should call update_Q_value before returning.  E.g.,
    update_Q_value(PREVIOUS_STATE, action, new_reward)

    PREVIOUS_STATE = new_state
    return # Nothing needs to be returned.

def choose_next_action(s, r, terminated=False):
     '''When the GUI or engine calls this, the agent is now in state s,
     and it receives reward r.
     If terminated==True, it's the end of the episode, and this method
      can just return None after you have handled the transition.

     Use this information to update the q-value for the previous state
     and action pair.  
     
     Then the agent needs to choose its action and return that.

     '''
     global INITIAL_STATE, PREVIOUS_STATE, LAST_ACTION, ALPHA, ACTIONS, GAMMA, STATES, Terminal_state, EPSILON_NOW, ALPHA_NOW
     global CUSTOM_EPSILON, CUSTOM_ALPHA
     # Unless s is the initial state, compute a new q-value for the
     # previous state and action.

     if (CUSTOM_EPSILON and EPSILON_NOW == 999):
         EPSILON_NOW = 0.6
     elif (CUSTOM_EPSILON):
         EPSILON_NOW = EPSILON_NOW - 0.000001
     else:
         EPSILON_NOW = EPSILON

     if (CUSTOM_ALPHA and ALPHA_NOW == 999):
         ALPHA_NOW = 0.2
     elif (CUSTOM_ALPHA):
         ALPHA_NOW = ALPHA_NOW - 0.00001
     else:
         ALPHA_NOW = ALPHA

     if not (s==INITIAL_STATE):
         # Compute your update here.
         # if CUSTOM_ALPHA is True, manage the alpha values over time.
         # Otherwise go with the fixed value.

         max_new_q = -999
         for a in ACTIONS:
             max_new_q = max(max_new_q, Q_VALUES[(s, a)])
         sample = r + GAMMA * max_new_q 
         new_qval = (1 - ALPHA_NOW) * Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] + (ALPHA_NOW * sample)

         # Save it in the dictionary of Q_VALUES:
         Q_VALUES[(PREVIOUS_STATE, LAST_ACTION)] = new_qval

         # Then let the Engine and GUI know about the new Q-value.
         update_Q_value(PREVIOUS_STATE, LAST_ACTION, new_qval)
         
     # Now select an action according to your Q-Learning criteria, such
     # as expected discounted future reward vs exploration.

     if USE_EXPLORATION_FUNCTION:
         # Change this if you implement an exploration function:
#*** ADD OR CHANGE CODE HERE ***
         print("You have not implemented an exploration function")

     # If EPSILON > 0, or CUSTOM_EPSILON is True,
     # then use epsilon-greedy learning here.
     # In order to access q-values, simply get them from the dictionary, e.g.,
     # some_qval = Q_VALUES[(some_state, some_action)]

#*** ADD OR CHANGE CODE HERE ***
     if is_valid_goal_state(s):
        some_action = 'Exit'
     elif terminated:
        some_action = None
     else:
        if random.random() < EPSILON_NOW:
            some_action = random.choice([x for x in ACTIONS if x not in ['Exit']])
        else:
            max_q_now = -999
            for a in ACTIONS:
                if(a != 'Exit'):
                    if Q_VALUES[(s, a)] > max_q_now:
                        max_q_now = Q_VALUES[(s, a)]
                        some_action = a


     LAST_ACTION = some_action # remember this for next time
     PREVIOUS_STATE = s        #    "       "    "   "    "
     return some_action

def return_Q_values(S, A):
   '''Return the dictionary whose keys are (state, action) tuples,
   and whose values are floats representing the Q values from the
   most recent call to one_step_of_VI. This is the normal case, and
   the values of S and A passed in here can be ignored.
   However, if no such call has been made yet, use S and A to
   create the answer dictionary, and use 0.0 for all the values.
   '''
   if(PREVIOUS_STATE != INITIAL_STATE):
      return Q_VALUES # placeholder
   else:
      for s in S:
         for a in A:
            Q_VALUES[s, a] = 0.0
      return Q_VALUES
Policy = {}
def extract_policy(S, A):

   global Policy
   Policy = {}
   # Add code here
   for s in S:
      max_Q = -999
      for a in A:
         if((s,a) in Q_VALUES and Q_VALUES[(s,a)] >= max_Q):
            Policy[s] = a
            max_Q = Q_VALUES[(s,a)]
   return Policy

