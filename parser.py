from action import Action
from agent import Agent
from formula import Literal, Negation, Conjunction, Disjunction, Knows, Top, Bot, Implication, Biimplication
from protocol import Protocol

from lark import Lark, exceptions, Transformer, Tree, v_args
from lark.indenter import Indenter
import sys


@v_args(inline=True)    # Affects the signatures of the methods
class LogicTreeTransformer(Transformer):
	'''
	This class transforms the information as parsed by the parser into
	the structure in which it can be used in the rest of the program.
	'''
	def __init__(self):
		self.vars = {}
		self._literals = []
		self._actions = []

	def start(self, literals, truth, actions, protocols, agents):
		# Is called by Central System, this is what will be returned as input
		return literals, truth, actions, protocols, agents

	def literals(self, *literals):
		# The list of literals. The literals later in input should match these
		self._literals = [str(literal) for literal in literals]
		self._literals.extend(["_true", "_false"])
		all_literals = [Literal(literal.value) for literal in literals]
		return all_literals

	def truth(self, *expr):
		# The list of true expressions
		return expr

	def actions(self, *actions):
		# The list of possible actions
		return actions

	def protocols(self, *protocols):
		# The list of possible protocols
		return protocols

	def agents(self, *agents):
		# The list of agents
		return agents

	def agent(self, agent_in, info, acts, goal):
		# The individual agents with their goals, knowledge, and actions
		new_agent = Agent(agent_in.value, goal, info, acts)
		return new_agent

	def protocol(self, name, if_, then):
		# The individual protocols with if- and then- conditions
		new_protocol = Protocol(name.value, if_, then)
		return new_protocol

	def action(self, name, pre, post):
		# The individual actions with pre- and post-conditions
		new_action = Action(name.value, pre, post)
		# The actions are stored for later reference
		self._actions.append({'name': name.value, 'act': new_action})
		return new_action

	def info(self, *sentence):
		# The information elements an agent possesses
		return sentence

	def acts(self, *actionname):
		# The actions as read in for agents, full information is collected locally
		acts = []
		for name in actionname:
			act = next((item for item in self._actions if item['name'] == name.value), False)
			if act is False:
				sys.exit("Error: {} is not a saved action".format(name))
			else:
				acts.append(act)
		return acts

	def goal(self, goal):
		# The goal of the agent
		return goal 

	def literal(self, literal):
		# The individual literals, these are checked to be valid
		if literal not in self._literals:
			sys.exit("Error: {} is not a literal".format(literal))
		if literal.value == '_true':
			return Top()
		if literal.value == '_false':
			return Bot()
		return Literal(literal.value)

	def conjunction(self, expr1, expr2):
		# Creating a conjuction
		return Conjunction(expr1, expr2)

	def disjunction(self, expr1, expr2):
		# Creating a disjunction
		return Disjunction(expr1, expr2)

	def implication(self, expr1, expr2):
		# Creating an implication
		return Implication(expr1, expr2)

	def biimplication(self, expr1, expr2):
		# Creating a bi-implication
		return Biimplication(expr1, expr2)

	def negation(self, expr):
		# Creating a negation
		return Negation(expr)

	def knows(self, agent, expr):
		# Creating a Knowledge statement
		return Knows(agent, expr)

class TreeIndenter(Indenter):
	'''
	This class defines how indents can be used in input to be parsed by the parser
	'''
	NL_type = '_NL'
	OPEN_PAREN_types = []
	CLOSE_PAREN_types = []
	INDENT_type = '_INDENT'
	DEDENT_type = '_DEDENT'
	tab_len = 2


def parse_input(title):
	'''
	This function opens the inputfile (with title as given), and inputs that 
	in the parser. The information contained in the input is returned.
	'''
	expr_parser = Lark(open('gram.lark'), parser="lalr", postlex=TreeIndenter(), transformer=LogicTreeTransformer())
	expression = expr_parser.parse

	path = './examples/' + title + '.txt'
	with open(path, "r") as file:
		parse_input = file.read()

	return expression(parse_input)

	
