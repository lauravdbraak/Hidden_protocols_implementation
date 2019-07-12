from kripkemodel import *
from formula import *
import pprint


class Relations():

	"""
	The class for the relations in the Kripke model.
	The relations:
		for all agents a dictionary from a state to a set of states
		each state in that set is not distinguishable from this one
	"""
	def __init__(self, model, agent_names):
		# Set up the relations for the model.
		self.model = model
		self.relations = {}
		for agent in agent_names:
			rel = self.relation_states(agent)
			self.relations[agent] = rel


	def relation_states(self, agent):
		# For each agent, set up the dictionary from state to set of states
		rel_states = {}
		for state in self.model.states:
			rel_states[state] = set(self.model.states)
		return rel_states

	def print_agent_states(self, agent):
		# Print all the states for the agent
		print("Agent {0}".format(agent))
		pp = pprint.PrettyPrinter(indent=4)
		pp.pprint(self.relations[agent])

	def get_agent_states(self, agent):
		# Get all states considered possible for this agent
		return self.relations[agent].keys()

	def get_reachable_states(self, state, agent):
		# From a state, return all states that the agent has a relation to
		reach = self.relations[agent]
		return reach[state]

	def contains_relation_for_agent(self, from_, to_, agent):
		# Boolean function for if a relation exists for an agent
		states = self.relations[agent]
		for key, vals in states:
			if key == from_ and to_ in vals:
					return True
		return False


	def remove_state(self, removal_state):
		# Remove a state from the relations

		# For all agents
		for agent in self.relations:
		# Remove state as key from states dictionary
			del self.relations[agent][removal_state]

			# Remove state as value from all state dictionaries
			remove = []
			reach = self.relations[agent]
			for state in reach:
				set_states = reach[state]
				if removal_state in set_states:
					remove.append((state,removal_state))
			for (state, remove_state) in remove:
				reach[state].remove(removal_state)
		# Check whether the removed state was the current point. If so, replace it
		self.model.check_true_state(removal_state)

	def remove_relations(self, agent, state_from, state_to):
		# Remove the relation from this state to that state for this agent
		reach = self.relations[agent]
		remove = []
		for state in reach:
			set_states = reach[state]
			if state == state_from:
				if state_to in set_states:
					remove.append((state, state_to))
		for (state, state_to) in remove:
			reach[state].remove(state_to)
		
	def private_announcement(self, message, agent):
		# Perform a private announcement to an agent
		reach = self.relations[agent]
		pos_states = []
		neg_states = []
		# For states for agent, determine if message evals true or false
		for state in reach:
			if message.evaluate(self.model, state):
				pos_states.append(state)
			else:
				neg_states.append(state)

		# Remove all connections between true and false evaluations both ways
		for p_state in pos_states:
			for n_state in neg_states:
				self.remove_relations(agent, p_state, n_state)
				self.remove_relations(agent, n_state, p_state)

	def private_belief_update(self, message, agent):
		# Updates the relations for an agent regarding their personal beliefs
		reach = self.relations[agent]
		# For all possible states
		for state in reach:
			sts = []
			# Consider all reachable states
			for st in reach[state]:
				# if the message evaluates as false, remove the link to that state
				if not message.evaluate(self.model, st):
					if st == state and st in self.model.trues:
						if self.model.verbose > 1:
							print("Removing reflexive relation {0} for message {1} and agent {2}\n State had values {3}".format(st, message, agent, self.model.state_map.states[st]))
					sts.append(st)
			for s in sts:
				self.remove_relations(agent, state, s)





