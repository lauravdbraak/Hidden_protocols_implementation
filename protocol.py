class Protocol():
	"""
	A class that keeps track of a protocol, w preconditions and postconditions """

	def __init__(self, name, preconditions, postconditions):
		'''
		:param name the name of the protocol
		:type name a string
		:param preconditions the preconditions for the protocol
		:type preconditions a parse Tree
		:param postconditions the postconditions for the protocol
		:type postconditions a parse Tree
		'''
		self.name = name
		self.preconditions = preconditions
		self.postconditions = postconditions

	def __str__(self):
		return "Protocol: {0} with preconditions {1} and postconditions {2}".format(self.name, self.preconditions, self.postconditions)