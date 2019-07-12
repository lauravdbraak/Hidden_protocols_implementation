class Action():
	"""
	A class to store each action with postconditions and preconditions"""

	def __init__(self, name, preconditions, postconditions):
		'''
		:param name the name of the action
		:type name a string
		:param preconditions the preconditions for the action
		:type preconditions a parse Tree
		:param postconditions the postconditions for the action
		:type postconditions a parse Tree
		'''
		self.name = name
		self.preconditions = preconditions
		self.postconditions = postconditions

	def __str__(self):
		return "Action: {0} with preconditions {1} and postconditions {2}".format(self.name, self.preconditions, self.postconditions)
