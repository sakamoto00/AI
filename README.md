# AI
Implementation of some important ideas in the AI world, including problem formulation, search algorithms, adversarial search, markov decision processes and Q-learning.

In the Problem Formulation, different kinds of games were formulated and put into framework of the classical theory of problem solving. Then, several searching algorithms including DFS, BFS, IDDFS and A* search were implemented and applied to the problem models.

In the Adversarial Search is the implementation of exploring two-person, zero-sum game playing using a family of games called "Toro-Tile Straight". This puts our agents into competition, adding lookahead (with the Minimax technique) and, optionally, pruning (with the alpha-beta method) and caching (with Zobrist hashing) to the search.

In Q-learning, the search theme continues here, except that now our agents operate in a world in which actions may have uncertain outcomes. The interactions are modeled probabilistically using the technique of Markov Decision Processes. It focuses on two approaches to having the agent maximize its expected utility: (1) by a form of planning, in which we assume that the parameters of the MDP (especially Transition Possiblity and Rewards) are known, which takes the form of Value Iteration, and (2) by an important form of reinforcement learning, called Q-learning, when the MDP functions are unknown to the agent.
