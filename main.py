from central_system import Central_System
import sys

# Set configuration inputs for the different examples.
lang_config = {'title' : "language", 'agent_names': ["Abe", "Britt"], 'turns' : [], 'rounds' : 1}
soc_config = {'title' : "social", 'agent_names': ["Kate", "Jane", "Anne"], 'turns' : ["Kate", "Jane", "Anne"], 'rounds' : 2}
# dipl_config = {'title' : "diplomatic", 'agent_names': ["Alice", "Bob"], 'turns' : [], 'rounds' : 1}


#Prompt the user for input
example = int(input("\nThis is the implementation for reasoning in hidden protocol situations. \nPlease enter the examples you wish to see.\nPlease enter 1 for the Language example, 2 for the Social example, or 3 for both.\n"))
if example not in range(1,4):
	sys.exit("Example chosen not one of 1, 2, or 3.")

verbose = int(input("Please enter how verbose you wish the output to be: 0, 1, or 2.\n0 gives only the results, 1 prints the choices of agents, 2 is debug mode.\n"))
if verbose not in range(0,3):
	sys.exit("Verbose level chosen not one of 0, 1, or 2.")

#Run examples
if example % 2 == 1:
	lang_cs = Central_System(lang_config, verbose)
	lang_cs.run_example()

if example > 1:
	soc_cs = Central_System(soc_config, verbose)
	soc_cs.run_example()

#Printing Results
if example % 2 == 1:
	lang_cs.print_results()
if example > 1:
	soc_cs.print_results()
