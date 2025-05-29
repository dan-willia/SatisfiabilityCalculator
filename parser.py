'''
See acknowledgements.

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