# Thesis
This repository contains the implementation created to supplement the masters thesis: Extracting Beliefs from Hidden Protocol Situations: Additions to the Existing Formalisation

Author: Laura van de Braak

Supervisor: Prof. Dr. Rineke Verbrugge

Date: 9 April 2018 - 12 July 2019


## To build
This implementation was built in python 3.5.3, using the Lark Library. 
Before running, ensure the following dependencies are installed via pip:

- lark-parser==0.6.6
- matplotlib==2.0.2
- networkx==1.11

## To run
To run the code, run `python main.py` from the command line. A terminal dialogue will then prompt for input regarding the example run and the verbose level of the output.

There are two examples: the language example and the social example, which are introduced below. It is possible to run either just one of the examples, or both. The verbose level will be the same for both examples, if both are run at the same time.

The language example runs quite fast, it will take a few seconds only. The social example may take up to 30 seconds to run, and will generally take at least 25 seconds.


## The examples
The textual version of the examples implemented is provided here for context.

### The Language example
Take two businessmen, a Brit and an American, who want to agree on a location for their meeting. The location is on 'the first floor'. Unbeknownst to the businessmen, they have a different meaning attached to that sentence. The concept of 'the first floor' of a building is culturally ambiguous. For American English speakers, they use this to refer to the ground floor - the floor on ground level. British English speakers will say this when referring to the next floor up from the ground floor. When the time for the meeting arrives, the businessmen will find themselves on different floors.

### The Social example
Consider a café in the 1950s, with three persons, Kate, Jane and Anne sitting across a table. Suppose Kate is gay and wants to know whether either of the other two is gay. She wants to convey the right information to the right person, without the other getting any idea of the information that is being communicated. She states: 'I am musical, I like Kathleen Ferrier's voice'. Jane, who is gay herself, immediately realizes that Kate is gay, whereas for Anne, the statement just conveys a particular taste in music.

Jane immediately wants to make sure that Kate knows she is gay, so she responds 'I agree, I especially liked her performance of Orfeo in Gluck's *Orfeo ed Euridice*'. The role of Orfeo, the male lead, is the one Kathleen Ferrier portrayed, and so to Kate it is clear that Jane is also gay. Meanwhile, Anne is still oblivious to the hidden message communicated.




