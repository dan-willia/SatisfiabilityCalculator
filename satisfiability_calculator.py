'''
The idea for the structure of this program comes from Programming, Principles and
Practice Using C++ by Bjarne Stroustrup. He guides the reader through the creation
of a commandline calculator (also involving a parser) starting in Unit 6. This is a
very similar program written in Python and involving the propositional calculus
instead of arithmetic.

The grammar for the parser is the following:
  Expression
    Term
    Expression '->' Term
    Expression '<->' Term
  Term
    Primary
    Term '^' Primary
    Term 'v' Primary
  Primary
    Secondary
    '~' Secondary
  Secondary
    Letters
    '(' Expression ')'
'''

import re

TOKENS = [
    ('ARROW', r'->'),
    ('DOUBLE_ARROW', r'<->'),
    ('AND', r'\^'),
    ('OR', r'v'),
    ('NOT', r'~'),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LETTER', r'[a-z]'),
    ('WS', r'\s+')
]

def tokenize(input_str):
  token_spec = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKENS)
  token_re = re.compile(token_spec)
  tokens = []
  for match in token_re.finditer(input_str):
    token_type = match.lastgroup
    token_value = match.group(token_type)
    if token_type == 'WS':
      continue # Skip whitespace
    tokens.append((token_type, token_value))
  return tokens

# Recursive descent parser
class Parser:
  def __init__(self, tokens, vars):
    self.tokens = tokens
    self.pos = 0
    self.vars = vars

  def current_token(self):
    return self.tokens[self.pos] if self.pos < len(self.tokens) else None

  def advance(self):
    self.pos += 1

  def match(self, expected_type):
    if self.current_token() and self.current_token()[0] == expected_type:
      self.advance()
      return True
    return False

  # Expression -> Term | Expression '->' Term | Expression '<->' Term
  def expression(self):
    node = self.term()
    while self.current_token() and self.current_token()[0] in ('ARROW', 'DOUBLE_ARROW'):
      token_type = self.current_token()[0]
      self.advance()
      right_node = self.term()
      if token_type == 'ARROW':
        node = not node or right_node
      if token_type == 'DOUBLE_ARROW':
        node = (not node or right_node) and (not right_node or node)
    return node

  # Term -> Primary | Term '^' Primary | Term 'v' Primary
  def term(self):
    node = self.primary()
    while self.current_token() and self.current_token()[0] in ('AND', 'OR'):
      token_type = self.current_token()[0]
      self.advance()
      right_node = self.primary()
      if token_type == 'AND':
        node = node and right_node
      if token_type == 'OR':
        node = node or right_node
    return node

  # Primary -> Secondary | '~' Secondary
  def primary(self):
    if self.match('NOT'):
      node = not self.secondary()
    else:
      node = self.secondary()
    return node

  # Secondary -> Letter | '(' Expression ')'
  def secondary(self):
    variables = self.vars

    if self.match('LPAREN'):
      node = self.expression()
      if not self.match('RPAREN'):
        raise ValueError("Missing closing parenthesis")
    elif self.current_token() and self.current_token()[0] == 'LETTER':
      node = self.current_token()[1]
      node = variables[node]
      self.advance()
    else:
      raise ValueError(f"Unexpected token: {self.current_token()}")
    return node

# Parse and build the parse tree
def parse(input_str, vars):
  tokens = tokenize(input_str)
  parser = Parser(tokens, vars)
  parse_tree = parser.expression()
  return parse_tree

 # Create all combinations of truth values of n variables
def bool_combs(n):
  if not n:
    return [[]]
  result = []
  for comb in bool_combs(n-1):
    result.append(comb + [True])
    result.append(comb + [False])
  return result

# Return a list of dictionaries, where each dict represents a row in a truth table
def bool_dict(vars):
  '''
  vars is a list of variables as strings, e.g. ['p', 'q']
  '''
  result = []
  for tv in bool_combs(len(vars)):
    result.append(dict(zip(vars, tv)))
  return result

'''
Using examples from p. 31, Rosen, 7th edition:

Entering (p v ~q) ^ (q v ~r) ^ (r v ~p) yields the answer that the statement is
satisfiable when p q r have the same truth value.

Entering (p v ~q) ^ (q v ~r) ^ (r v ~p) ^ (p v q v r) ^ (~p v ~q v ~r) yields the
answer that the statement is not satisfiable.
'''
def main(): 
    print("Welcome to the satisfiability calculator.")
    print("Enter a proposition to see if and under what conditions it is satisfiable.")
    print("We support the following operators: 'v', '^', '~', '->', '<->', and letters for variables.")
    userExpression = input("Enter a proposition below:\n")
    userVariables = input("Enter the variables contained in your expression, separated by a space:\n")
    userVariables = userVariables.rsplit(" ")

    result = []
    var_dict = bool_dict(userVariables)
    for d in var_dict:
        eval = parse(userExpression, d)
        if eval:
          result.append(eval)

    if True not in result:
        print("The statement is not satisfiable.")
    elif len(result) == 2**len(userVariables):
        print("The statement is a tautology.")
    else:
        print("The statement is satisfied under the following conditions:")
        for i in range(len(result)):
            if result[i] == True:
                print(var_dict[i])
            
if __name__ == "__main__":
    main()