from action import *
from formula import *

import random

class Agent():

	"""
	The Agent class. This contains all methods the agents use to reason.
	The agents choose actions to perform that will help them achieve their goal.

	"""

	def __init__(self, name, goal, knowledge, action=[]):
		# create the agent with a name, goal, knowledge, and possible actions
		self.set_goal(goal)
		self.name = name
		self.actions = action 
		self.knowledge = []
		self.set_knowledge(knowledge)

	def __str__(self):
		return "Agent {0} has goal ({1}), which is {2}".format(self.name, self.goal, self.achieved())

	def print_states(self):
		# Print the states the agent considers possible
		self.model.print_agent_states(self)

	def set_knowledge(self, knowledge):
		# Separate function to set knowledge and add knowledge at a later stage.
		for info in knowledge:
			self.knowledge.append(info)

	def set_model(self, model):
		# The agent can access the Kripke model, this is added soon after initialisation
		self.model = model

	def simplify_knowledge(self):
		# Simplify the formulas in the knowledge
		for info in self.knowledge:
			info = info.simplify()

	def add_actions(self, actions):
		# Add new actions to the list of possible actions
		self.actions.append(actions)

	def set_goal(self, goal):
		# Set the goal. If there is none, set to Top, which is always true.
		if goal == 0:
			self.goal = Top()
		else:
			self.goal = goal

	def change_goal(self, goal):
		# Change the goal
		self.goal = goal

	def eval_goal(self):
		# Evaluate if the goal is true for the agent.
		return self.model.eval_goal(self.goal, self)

	def find_available_actions(self, model, verbose):
		# Find available actions for the agent and return the list
		available = []
		states = model.get_agent_states(self)
		for action in self.actions:
			count = 0
			if verbose > 1:
				print(action['act'].preconditions)

			# If the agent knows the preconditions of the action, it is available
			for state in states:
				if Knows(self, action['act'].preconditions).evaluate(model, state): 
					count += 1
			if verbose > 1:
				print("\t {0} out of {1} states have value True".format(count, len(states)))
			if count == len(states):
				available.append(action)
		return available

	def eval_action(self, action, available_actions):
		# To evaluate an action, test it in a copy of the model
		copy_model = Kripke_Model.from_kripke(self.model)
		return copy_model.eval_action(action, self, available_actions)


	def eval_score(self, scores, available_actions, verbose):
		# Choose the best action from the scores given
		max_score = max(scores.values())
		best = [key for key, value in scores.items() if value == max_score]
		if verbose > 0:
			print("Best score is {0} for actions {1}".format(max_score, best))
		# If there is only one with the highest score, return that one
		if len(best) == 1:
			return best[0]
		# If there are no best actions: choose one of the available actions randomly
		elif len(best) == 0: 
			return random.choice(available_actions)
		# If there are multiple best actions, choose one of the best ones randomly
		else: 
			return random.choice(best)

	def choose_action(self, verbose):
		# Out of all actions possible, choose best action for goal
		if verbose > 0:
			print("Choosing actions for agent {0}".format(self.name))
		self.simplify_knowledge()

		# Find which actions are possible, if there are none, return None
		available_actions = self.find_available_actions(self.model, verbose)
		if len(available_actions) == 0:
			return None

		# Score the available actions
		scores = {}
		for action in available_actions:
			scores[action['act'].name] = (self.eval_action(action, available_actions))

		# Return the best of the actions
		return self.eval_score(scores, available_actions, verbose)

	def achieved(self):
		# A check to see if the goal is achieved, used when calling str() on agent
		ach = self.eval_goal()
		if ach == 1:
			return "achieved"
		elif ach == 0:
			return "currently believed false"
		return "not yet achieved"

