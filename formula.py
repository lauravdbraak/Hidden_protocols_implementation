"""
A document containing the classes to represent a formula.
"""
from kripkemodel import *
from abc import ABC, abstractmethod as abstract 

class Formula(ABC):
	"""
	This abstract class is the base class for all specific types of formula.
	A formula can be simplified, evaluated, and can return a string version of the formula.
	"""
	def __to_str__(self):
		# Return self in parentheses when not overwritten
		return '(' + str(self) + ')'

	@abstract
	def simplify(self):
		"simplify the formula"

	@abstract
	def evaluate(self):
		"evaluate the formula"

class Top(Formula):
	"""
	The Top is always true.
	"""
	def __to_str__(self):
		return "_true"

	def __str__(self):
		return self.__to_str__()

	def simplify(self):
		return self

	def evaluate(self, model, state):
		return True

class Bot(Formula):
	"""
	The Bot is always false.
	"""
	def __to_str__(self):
		return "_false"

	def __str__(self):
		return self.__to_str__()

	def simplify(self):
		return self

	def evaluate(self, model, state):
		return False

class Literal(Formula):
	"""
	The Literal is the most basic of formulas, the atomic element.
	"""
	def __init__(self, lit):
		self.formula = lit 

	def __to_str__(self):
		return self.formula

	def __str__(self):
		return self.__to_str__()

	def simplify(self):
		return self

	def evaluate(self, model, state):
		return model.eval_in_state(state, self)


class Negation(Formula):
	"""
	The Negation class
	"""
	def __init__(self, neg):
		self.formula = neg

	def __to_str__(self):
		return '~ ' + self.formula.__to_str__()

	def __str__(self):
		return self.__to_str__()

	def simplify(self):
		if isinstance(self.formula, Negation):
			return self.formula.formula.simplify()
		return Negation(self.formula.simplify())

	def evaluate(self, model, state):
		if self.formula.evaluate(model, state):
			return False
		return True


class Conjunction(Formula):
	"""
	The Conjunction class
	"""
	def __init__(self, *args):
		self.conjuncts = args

	def __str__(self):
		return ' & '.join(conj.__to_str__() for conj in self.conjuncts)

	def flatten(self):
		# Returns a new Conjunction in which all conjuncts are not a Conjunction class. (e.g. ((A & B) & C) becomes (A & B & C))
		flat_conjuncts = []
		for conj in self.conjuncts:
			if isinstance(conj, Conjunction):
				flat_conjuncts.extend(conj.flatten().conjuncts)
			else:
				flat_conjuncts.append(conj)
		return Conjunction(*flat_conjuncts)

	def simplify(self):
		# A simplification of a conjunction is the conjunction of the simplification of all its conjuncts.
		new_conjuncts = []
		for conj in self.flatten().conjuncts:
			if isinstance(conj, Conjunction):
				new_conjuncts.extend(conj.simplify())
			else:
				new_conjuncts.append(conj.simplify())
		if len(new_conjuncts) == 1:
			return new_conjuncts[0]
		return Conjunction(*new_conjuncts)


	def evaluate(self, model, state):
		# If any conjunct is false, the conjunction is False, else True
		for conj in self.simplify().conjuncts:
			if not conj.evaluate(model, state):
				return False
		return True


class Disjunction(Formula):
	"""
	The Disjunction class
	"""
	def __init__(self, *args):
		self.disjuncts = args

	def __str__(self):
		return ' | '.join(disj.__to_str__() for disj in self.disjuncts)

	def flatten(self):
		# Returns a new Disjunction in which all disjuncts are not a Disjunction class. (e.g. ((A | B) | C) becomes (A | B | C))
		flat_disjuncts = []
		for disj in self.disjuncts:
			if isinstance(disj, Disjunction):
				flat_disjuncts.extend(disj.flatten().disjuncts)
			else:
				flat_disjuncts.append(disj)
		return Disjunction(*flat_disjuncts)

	def simplify(self):
		# A simplification of a disjunction is the disjunction of the simplification of all its disjuncts.
		new_disjuncts = []
		for disj in self.flatten().disjuncts:
			if isinstance(disj, Disjunction):
				new_disjuncts.extend(disj.simplify())
			else:
				new_disjuncts.append(disj.simplify())
		if len(new_disjuncts) == 1:
			return new_disjuncts[0]
		return Disjunction(*new_disjuncts)

	def evaluate(self, model, state):
		# If any disjunct is True, the disjunction is True, else False
		for disj in self.simplify().disjuncts:
			if disj.evaluate(model, state):
				return True
		return False

class Implication(Formula):
	"""
	The Implication class
	"""
	def __init__(self, formula1, formula2):
		self.formula1 = formula1
		self.formula2 = formula2

	def __to_str__(self):
		return self.formula1.__to_str__() + ' -> ' + self.formula2.__to_str__()

	def __str__(self):
		return self.__to_str__() 

	def simplify(self):
		return Implication(self.formula1.simplify(), self.formula2.simplify())

	def evaluate(self, model, state):
		# If the antecendent is not true, or if the consequent is true, the implication is true
		if (not self.formula1.evaluate(model, state)) or self.formula2.evaluate(model, state):
			return True
		return False

class Biimplication(Formula):
	"""
	The Bi-implication class
	"""
	def __init__(self, formula1, formula2):
		self.formula1 = formula1
		self.formula2 = formula2

	def __to_str__(self):
		return self.formula1.__to_str__() + ' <-> ' + self.formula2.__to_str__()

	def __str__(self):
		return self.__to_str__() 

	def simplify(self):
		return Biimplication(self.formula1.simplify(), self.formula2.simplify())

	def evaluate(self, model, state):
		# If the left side evaluates the same as the right side, it is true
		return self.formula1.evaluate(model, state) == self.formula2.evaluate(model, state)

class Knows(Formula):
	"""
	The Knowledge operator class, takes both the agentname and a formula. 
	"""
	def __init__(self, agentname, form):
		self.agent = agentname
		self.formula = form

	def __to_str__(self):
		return ' #_' + self.agent + ' ' + self.formula.__to_str__()

	def __str__(self):
		return self.__to_str__() 

	def simplify(self):
		return Knows(self.agent, self.formula.simplify())

	def evaluate(self, model, state):
		# If in all states reachable, the formula is true, the Knowledge is true
		states = model.get_reachable_states(state, self.agent)
		for st in states:
			if not self.formula.evaluate(model, st):
				return False
		return True



