from formula import *
from state_map import *
from relations import *
import copy	
import random

class Kripke_Model():
	"""
	The Kripke Model class. It stores the states and relations
	It can be update to reflect the current information
	"""
	def __init__(self, literals, truth, agent_names, verbose):
		# Set up the relations matrix and the State map
		self.verbose = verbose
		self.state_map = State_Map(literals) #list of dicts with lits and values
		self.agent_names = agent_names
		self.states = list(range(len(self.state_map.states)))
		self.relations = Relations(self, agent_names)
		self.true_state = self.determine_true_state(truth)

	@classmethod
	def from_kripke(cls, old_model):
		# Allows the user to copy the model without overwriting.
		model = cls.__new__(cls)
		model.verbose = old_model.verbose
		model.state_map = copy.deepcopy(old_model.state_map)
		model.agent_names = old_model.agent_names

		model.states = copy.deepcopy(old_model.states)
		model.relations = copy.deepcopy(old_model.relations)
		model.trues = old_model.trues
		model.true_state = old_model.true_state
		model.verbose = old_model.verbose

		return model

	def print_true_state(self):
		# Print the point from which evaluation happens currently
		print("True state: {0}, with values: {1}".format(self.true_state, self.state_map.states[self.true_state]))

	def print_state_map(self):
		# Print the entire state map
		self.state_map.print_states()

	def print_agent_states(self, agent):
		# Print all available states for the agent
		self.relations.print_agent_states(agent)

	def print_model(self):
		# Print the entire model
		print("True states: {0}".format(self.trues))
		self.print_state_map()
		for agent in self.agent_names:
			self.print_agent_states(agent)

	def determine_true_state(self, truth):
		# Determine points for the model and chosose one to reason from
		self.trues = []
		for expr in truth:
			expr_truth = []
			for state in self.states:
				if expr.evaluate(self, state):
					expr_truth.append(state)
			# list true worlds
			if self.trues == []:
				self.trues.extend(expr_truth)
			else:
				self.trues = [st for st in self.trues if st in expr_truth]

		if len(self.trues) == 1:
			return self.trues[0]
		else:
			true = random.choice(self.trues)
			if self.verbose > 1:
				print("There is more than one true world: {0}, \nwe chose {1} with values {2}".format(self.trues, true, self.state_map.states[true]))
			return true

	def check_true_state(self, removal_state):
		# check if true state has been removed. If it has, choose a new one.
		if removal_state in self.trues:
			self.trues.remove(removal_state)
			if removal_state == self.true_state:
				assert (len(self.trues) > 0), "No true worlds left after removal of {0}".format(removal_state)
				self.true_state = random.choice(self.trues)
				if self.verbose > 1:
					print("True state {0} removed, new true state is :".format(removal_state))
					self.print_true_state()


	def get_agent_states(self, agent):
		# Get the states reachable for an agent
		return self.relations.get_agent_states(agent.name)		

	def get_reachable_states(self, state, agent):
		# Return the set of states the agent can reach from current state
		if state == -1:
			state = self.true_state

		if isinstance(agent, str):
			return self.relations.get_reachable_states(state, agent)
		return self.relations.get_reachable_states(state, agent.name)

	def eval(self, literal):
		# Evaluate a literal in the true state
		return self.eval_in_state(self.true_state, literal)

	def eval_in_state(self, state, literal):
		# Evaluate a literal in the state mentioned.
		# If state passed along is -1, that refers to the true state
		if state == -1:
			return self.state_map.eval_in_state(self.true_state, literal)
		return self.state_map.eval_in_state(state, literal)

	def eval_action(self, action, agent, available_actions):
		""" Evaluate the worth of this action for goal
		If postconditions enable goal: score = 3
		If postconditions have pre for new action: score = 1
		If neither of these: score = 0
		Optional to add later: if new action would enable goal: score = 2
		"""

		# Execute the action in the model (happens only in a copy)
		post = action['act'].postconditions
		self.public_announcement(post)

		# Check if goal is true
		if agent.eval_goal() == True:
			return 3
		# Check if new actions are possible
		else:
			if self.verbose > 0:
				print("Checking if new actions are possible")
			acts = agent.find_available_actions(self, self.verbose)
			new = 0
			for act in acts:
				if act not in available_actions:
					new += 1
			if new > 0:
				return 1
			return 0

	def eval_goal(self, goal, agent):
		"""
		Evaluate the goal for the agent:
		if for all states goal returns true, return true
		if all are false, return false
		if a mix, return -1
		"""
		trues = 0
		falses = 0
		reach = self.get_agent_states(agent)
		# For all possible states for the agent evaluate goal
		for state in reach:
			if goal.evaluate(self, state):
				trues += 1
			else:
				falses += 1
		# If all states evaluate the goal as true: return 1
		if trues == len(reach):
			return 1
		elif falses == len(reach):
			return 0
		else:
			return -1

	def remove_state(self, state):
		# Remove a state from the model, including from the relations and the statemap
		self.relations.remove_state(state)
		self.state_map.remove_state(state)
		self.states.remove(state)

	def public_announcement(self, message): 
		# Perform a public announcement
		
		# Remove states in which the message is not true
		remove = []
		for state in self.states:
			if not message.evaluate(self, state):
				remove.append(state)
		for state in remove:
			self.remove_state(state)

	def private_announcement(self, message, agent):
		# Perfom a private announcement
		# for this agent, remove all connections between states that disagree on value of message
		self.relations.private_announcement(message, agent.name)

	def private_belief_update(self, message, agent):
		# Update the private beliefs for the agent with this message
		self.relations.private_belief_update(message, agent.name)



	