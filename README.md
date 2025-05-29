A command-line program for determining satisfiability conditions in the propositional calculus.

sat_calc_for_logical_validity.ipynb is a walkthrough of sorts.

This project was created in my free time during the first few weeks of CSPB2824 
at the University of Colorado, Boulder, taught by Elizabeth Stade and Cailyn Craven,
in Fall 2024.

The inspiration to write a satisfiability calculator came from computer project 3
on p. 113 of Rosen's Discrete Mathematics (7th Ed).

I got the idea to use a recursive descent parser from Bjarne Stroustrup's walkthrough of
a desktop calculator implementation in PPP 2nd Ed (Units 6, 7). I wrote the abstract
grammar following Stroustrup's example (see Unit 6, Section 4 of PPP 2nd Ed; see parse.py for the grammar tree). I then
gave that to ChatGPT to generate the recursive descent parser in the parser.py file.
Various small tweaks were needed to get the LLM-generated parser working properly. 
For example, the clumsy way of dealing with variables by having the user pass them in 
manually, which are then passed to the parser, is my own.

The bool_combs function in this file is taken from user2390182 on Stackoverflow
(https://stackoverflow.com/questions/54568536/generate-all-possible-values-for-variables-with-recursion).

The rest of the functions and logic are my own. 
