from action import *
from agent import *
from formula import *
from parser import *
from protocol import *
from show_kripke import *


class Central_System():
	"""

	The central system (cs) that will take on the running of the simulation. 
	It takes all the agents, protocols and information on turntaking. 
	After initialising the agents with their information, the cs will loop over
	the agents according to the turntaking method, asking them for actions. After
	an agents has chosen an action, the cs will update the example and all agents 
	according to the information contained in the protocols, and turn to the
	next agent. """

	def __init__(self, config, verbose):
		"""
		Initialises the central system

		:param config: contains the title, number of agents and turntaking system
		:type config: array with a string, an int and an array
		:param verbose: contains the verbose level, 0 only prints results, 1 prints run, 
		2 prints debug comments
		:type verbose: int
		"""
		self.title = config['title']
		self.verbose = verbose
		# Collecting the full input from the input file
		self.library, truth, actions, self.protocols, agents = parse_input(config['title'])
		self.actions = {action.name : action for action in actions}
		# Creating the agents
		self.agent_names = config['agent_names']
		self.agents = {key : value for (key, value) in zip(self.agent_names, agents)}
		# Setting game mechanics
		self.setup_turns(config['turns'])
		self.rounds = config['rounds']
		# Setting up Kripke Model
		self.model = Kripke_Model(self.library, truth, self.agent_names, self.verbose)
		# Creating list of performed actions to use later
		self.performed_actions = []

		if self.verbose > 0:
			print("Setup of {0} example complete.".format(self.title))

		# Initialising beliefs agents
		self.setup_agent_beliefs()
		if self.verbose > 0:
			print("Set up agent beliefs.\n")

	def setup_turns(self, turns):
		# Sets the turn order for asking agents for actions
		self.turns = []
		# If no order is given, use alphabetical order
		if turns == []:
			self.turns = sorted(self.agent_names, key=str.lower)
		# If only some agents are named in order, first do those, then the rest in alphabetical order
		elif len(turns) < len(self.agent_names):
			extra = [ag for ag in self.agent_names if ag not in turns]
			self.turns = turns
			self.turns.extend(sorted(extra, key=str.lower))
		# If all agents have a turn assigned already, use that order
		else:
			self.turns = turns

	def setup_agent_beliefs(self):
		# Set up the agents' initial beliefs
		for agent in self.agents.values():
			# Give the agent access to Kripke Model
			agent.set_model(self.model)
			# Update the agent's belief in the Kripke model
			for message in agent.knowledge:
				self.model.private_belief_update(message, agent)
		if self.verbose > 1:
			self.print_results()

	def run_example(self):
		'''
		runs program by executing protocols, and asking agents for actions
		'''

		# Check possible protocol updates
		self.execute_available_protocols()

		# Until the set number of rounds is completed, ask agents in turn for actions
		for i in range(self.rounds):
			if self.verbose > 0:
				print("\n Round {0}:".format(i+1))
			for t in self.turns:
				agent = self.agents[t]
				if self.verbose > 0:
					print("\n {0}'s turn.\n".format(agent.name))

				# Find the action the agent chooses
				act = agent.choose_action(self.verbose)
				if self.verbose > 0:
					print("{0} chose {1}".format(agent.name, act))
				#execute the action
				if not act == None:
					self.execute_action(agent, self.actions[act])
				if self.verbose > 1:
					self.print_results()
		if self.verbose > 0:
			print("Run of example {0} is complete.\n".format(self.title))


	def execute_available_protocols(self):
		# Executes available protocols
		available = []
		for prot in self.protocols:
			if prot.preconditions.evaluate(self.model, self.model.true_state):
				self.model.public_announcement(prot.postconditions)
			if self.verbose > 0:
				print("protocol {0} executed. \n".format(str(prot)))

	def execute_action(self, agent, action):
		# Executes the action chosen, and stores it in performed actions list
		self.performed_actions.append([agent.name, action.name])
		self.model.public_announcement(action.postconditions)

	def eval_results_in_all_true_states(self):
		# Evaluate results in all possible true states (can be many)
		for state in self.model.trues:
			self.print_results(state)

	def print_results(self, state=-1):
		# Prints the results for the example run
		print("\n {0} example:\nPerformed actions: {1}\n".format(self.title.title(), self.performed_actions))

		# Show the valuations for literals in the true state
		if state == -1:
			self.model.print_true_state()
		else:
			print("True state: {0}, with values: {1} \n".format(state, self.model.state_map.states[state]))

		# For every agent, show their beliefs on the key literals in the example run
		for agent in self.agents:
			print(str(self.agents[agent]))
			if self.title == 'social':
				print("Agent {0} believes that: \n\t _gayjane is {1} \n\t _gaykate is {2} \n\t _gayanne is {3}\n".format(agent, Knows(agent, Literal("_gayjane")).evaluate(self.model, -1), Knows(agent, Literal("_gaykate")).evaluate(self.model, state), Knows(agent, Literal("_gayanne")).evaluate(self.model, state)))

			if self.title == 'language':
				ground = Knows(agent, Literal('_ground')).evaluate(self.model, state)
				goal = Disjunction(Knows(agent, Literal('_ground')), Knows(agent, Negation(Literal('_ground')))).evaluate(self.model, state)
				k_goal = Knows(agent, Disjunction(Knows(agent, Literal('_ground')), Knows(agent, Negation(Literal('_ground'))))).evaluate(self.model, state)
				print("Agent {0} believes that the statement: 'the meeting is on the ground floor' is {1}.\n".format(agent, ground))

	def print_states(self):
		# Prints all states in the model, including which ones each agent can access
		print("Printing all states:\n")
		self.model.print_state_map()
		print(self.model.states)
		print("\nPrinting all agents with states:\n")
		for agent in self.agents:
			print("Agent {0} has states: ".format(agent))
			self.model.print_agent_states(agent)






