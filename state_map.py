from agent import *
from formula import *

import itertools
import pprint


class State_Map():
	"""
	The class to create a state map. 
	This contains the valuations of literals for every state
	"""

	def __init__(self, literals):
		# Set up state map for every combination of truth in literals
		self.states = {}
		lit_options = list(itertools.product([False,True], repeat =len(literals)))
		for index, option in enumerate(lit_options):
			state_content = self.create_state(literals, option)
			self.states[index] = state_content


	def create_state(self, literals, option):
		# Create the full combination for a state
		state = {lit.formula : val for (lit, val) in zip(literals, option)}
		return state 

	def __str__(self):
		return "State Map: {0}".format(self.states)

	def print_states(self):
		# Print the states legibly
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(self.states)

	def eval_in_state(self, state, literal):
		# Evaluate a literal in the state mentioned
		temp = self.states[state]
		return temp[literal.formula]

	def remove_state(self, state):
		# Remove a state from the state map
		del self.states[state]