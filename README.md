# SatisfiabilityCalculator
A command-line program to evaluate the satisfiability of logical propositions using propositional calculus. Inspired by the command-line calculator example from Programming: Principles and Practice Using C++ by Bjarne Stroustrup. This implementation is written in Python for logical operations.

## Features

- Parses and evaluates logical expressions with the following operators:
  - `v` : Logical OR
  - `^` : Logical AND
  - `~` : Logical NOT
  - `->` : Logical Implication
  - `<->` : Logical Bi-implication
- Generates truth tables for provided variables.
- Determines whether a logical expression is:
  - Satisfiable
  - A tautology
  - Unsatisfiable
- Provides detailed output of conditions under which the expression is satisfied.

## Grammar

The grammar for the recursive descent parser is as follows:

- Expression
  - Term
  - Expression '->' Term
  - Expression '<->' Term
- Term
  - Primary
  - Term '^' Primary
  - Term 'v' Primary
- Primary
  - Secondary
  - '~' Secondary
- Secondary
  - Letters
  - '(' Expression ')'

## How to Use

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/satisfiability-calculator.git
   cd satisfiability-calculator
2. ```bash
   python3 satisfiability_calculator.py
3. Enter a proposition using the supported operators and specify the variables.

## Example Input
- Proposition: ```(p v ~q) ^ (q v ~r) ^ (r v ~p)```
- Variables: ```p q r```

## Example Output
```
The statement is satisfied under the following conditions:
{'p': True, 'q': True, 'r': True}
{'p': False, 'q': False, 'r': False}
```
## Testing
You can test the program by running different logical propositions as inputs. Some examples from Discrete Mathematics and Its Applications by Rosen are included in the code comments.

## Future Enhancements
Add support for additional logical operators (e.g., XOR, NAND, NOR).
Implement a graphical user interface (GUI) for easier interaction.
Optimize performance for large-scale logical expressions.

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.

## Acknowledgments
Inspired by the command-line calculator example in Programming: Principles and Practice Using C++ by Bjarne Stroustrup.
Examples and test cases referenced from Discrete Mathematics and Its Applications by Kenneth H. Rosen.
