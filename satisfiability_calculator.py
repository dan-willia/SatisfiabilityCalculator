'''
Acknowledgements

This project was created in my free time during the first few weeks of CSPB2824 
at the University of Colorado, Boulder, taught by Elizabeth Stade and Cailyn Craven,
in Fall 2024.

The inspiration to write a satisfiability calculator came from computer project 3
on p. 113 of Rosen's Discrete Mathematics (7th Ed).

I got the idea to use a recursive descent parser from Bjarne Stroustrup's walkthrough of
a desktop calculator implementation in PPP 2nd Ed (Units 6, 7). I wrote the abstract
grammar following Stroustrup's example (see Unit 6, Section 4 of PPP 2nd Ed). I then
gave that to ChatGPT to generate the recursive descent parser in the parser.py file.
Various small tweaks were needed to get the LLM-generated parser working properly. 
For example, the clumsy way of dealing with variables by having the user pass them in 
manually, which are then passed to the parser, is my own.

The bool_combs function in this file is taken from user2390182 on Stackoverflow
(https://stackoverflow.com/questions/54568536/generate-all-possible-values-for-variables-with-recursion).

The rest of the functions and logic are my own. 

'''

from parser import *

def bool_combs(n: int) -> list[list[bool]]:
  """
  Recursively creates all combinations of truth values for n variables.
  Return value will be a (2**n)-long list, with each element an n-long list
  of bools. 
  
  >>> bool_combs(1)
  [[True], [False]]
  
  >>> bool_combs(2)
  [[True, True], [True, False], [False, True], [False, False]]
  """
  
  if n == 0:
    return [[]]
  
  result = []
  for comb in bool_combs(n-1):
    result.append(comb + [True])
    result.append(comb + [False])
  
  assert len(result) == 2**n
  assert len(result[0]) == n
  
  return result

def create_tt(vars: list[str]) -> list[dict[str: bool]]:
  '''
  Returns a truth table given a list of variables.
  
  >>> create_tt(['p'])
  [{'p': [True]}, {'p': [False]}]
  
  >>> create_tt(['p', 'q'])
  [
    {'p': True, 'q': True},
    {'p': True, 'q': False},
    {'p': False, 'q': True},
    {'p': False, 'q': False}
   ]
  '''
  result = []
  truth_assignments = bool_combs(len(vars))
  for ta in truth_assignments:
    result.append(dict(zip(vars, ta)))
  return result

'''
Using examples from p. 31, Rosen:

Entering (p v ~q) ^ (q v ~r) ^ (r v ~p) yields the answer that the statement is
satisfiable when p q r have the same truth value.

Entering (p v ~q) ^ (q v ~r) ^ (r v ~p) ^ (p v q v r) ^ (~p v ~q v ~r) yields the
answer that the statement is not satisfiable.
'''
def main(): 
    print("Welcome to the satisfiability calculator.")
    print("Enter a proposition to see if and under what conditions it is satisfiable.")
    print("We support the following operators: 'v', '^', '~', '->', '<->', and letters for variables.")
    # userExpression = input("Enter a proposition below:\n")
    # print(f"You entered {userExpression}")
    # userVariables = input("Enter the variables contained in your expression, separated by a space:\n")
    # userVariables = userVariables.rsplit(" ")
    
    userExpression = "(p v ~q) ^ (q v ~r) ^ (r v ~p)"
    userVariables = ['p', 'q', 'r']

    result = []
    tt = create_tt(userVariables)
    
    # evaluate expression for each truth assignment in truth table
    for ta in tt:
        eval = evaluate(userExpression, ta)
        # print(f"evaluated {ta} as {eval}")
        result.append(eval)

    if True not in result:
        print("The statement is not satisfiable.")
    elif False not in result:
        print("The statement is a tautology.")
    else:
        print("The statement is satisfied under the following conditions:")
        for i in range(len(result)):
            if result[i] == True:
                print(tt[i])
            
if __name__ == "__main__":
    main()
    