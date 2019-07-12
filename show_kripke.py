import networkx as nx
import matplotlib.pyplot as plt

"""
Code to print the Kripke model as graph, not currently used.
"""

def save_visual(graph, version):
	# save the visual to a file
	nx.draw(graph)
	plt.savefig("../fig/Kripke_{0}.png".format(version)) # save as png
	# plt.show() # display

def create_visual_kripke_for_agent(model, agent, version):
	# create a graph from kripke input
	graph = nx.DiGraph()
	states = [str(x) for x in model.states]
	graph.add_nodes_from(model.states)
	rel = model.relations.relations[agent]
	for state in rel:
		for st in rel[state]:
			graph.add_edge(state, st)
	# save the graph to a file
	save_visual(graph, version)

def create_visual_kripke(model, version):
	# Call the creation function for each agent
	for agent in model.agent_names:
		create_visual_kripke_for_agent(model, agent, version)