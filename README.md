# Lispy: A Scheme Interpreter in Python 3.13

An implementation of a Scheme/Lisp interpreter **Based on the original [Lispy](https://norvig.com/lispy.html) by Peter Norvig**, written in Python 3.13.


## Features

- **Python 3.13 Syntax**: Uses pattern matching, union types (`|`), and type hints
- **Core Lisp Features**: Variables, functions, conditionals, recursion, and list operations
- **Built-in Functions**: Arithmetic, comparison, list manipulation, and mathematical functions
- **Interactive REPL**: Command-line interface for interactive programming
- **Tests**: Full test suite using pytest with 20+ test cases
- **Error Handling**: Proper error messages and exception handling


## Files

- `lis.py` - The main interpreter implementation
- `test_lis.py` - Test suite
- `demo_lis.py` - Interactive demo with examples
- `requirements.txt` - Project dependencies

## Setup

### Create Virtual Environment and Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On macOS/Linux
# or
venv\Scripts\activate     # On Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Interpreter

```bash
# Activate virtual environment first
source venv/bin/activate

# Interactive REPL
python3 lis.py

# Run tests with pytest
pytest test_lis.py -v

# Or run tests directly
python3 test_lis.py

# Run demo with examples
python3 demo_lis.py
```

### Basic Examples

```scheme
; Arithmetic
(+ 1 2 3)           ; => 6
(* 4 5)             ; => 20
(- 10 3)            ; => 7
(/ 15 3)            ; => 5.0

; Variables
(define x 10)
(define y (* x 2))
y                   ; => 20

; Functions
(define square (lambda (x) (* x x)))
(square 5)          ; => 25

; Conditionals
(if (> 5 3) 'yes 'no)  ; => yes

; Lists
(define my-list '(1 2 3 4))
(car my-list)       ; => 1
(cdr my-list)       ; => (2 3 4)
(length my-list)    ; => 4

; Recursion
(define factorial 
  (lambda (n) 
    (if (<= n 1) 
        1 
        (* n (factorial (- n 1))))))
(factorial 5)       ; => 120
```

## Supported Operations

### Arithmetic
- `+`, `-`, `*`, `/` - Basic arithmetic (variadic for + and *)
- `abs`, `max`, `min`, `round` - Mathematical functions

### Comparison
- `>`, `<`, `>=`, `<=`, `=` - Comparison operators
- `eq?`, `equal?` - Equality testing

### List Operations
- `car` - First element of list
- `cdr` - Rest of list (all but first)
- `cons` - Construct list
- `list` - Create list from arguments
- `append` - Concatenate lists
- `length` - List length
- `null?` - Test for empty list

### Predicates
- `number?` - Test if number
- `symbol?` - Test if symbol
- `list?` - Test if list
- `procedure?` - Test if function

### Control Flow
- `if` - Conditional expression
- `quote` - Literal data
- `define` - Variable/function definition
- `set!` - Variable assignment
- `lambda` - Function creation
- `begin` - Sequential execution

### Higher-Order Functions
- `apply` - Apply function to list of arguments
- `map` - Apply function to each element of list


## Testing

The test suite uses pytest and includes:

- Basic arithmetic operations
- Variable definition and assignment
- Lambda functions and recursion
- List operations and predicates
- Error handling and edge cases
- Performance benchmarks

### Run Tests

```bash
# Activate virtual environment
source venv/bin/activate

# Run all tests with verbose output
pytest test_lis.py -v

# Run tests with short traceback on failures
pytest test_lis.py -v --tb=short

# Run specific test
pytest test_lis.py::test_basic_arithmetic -v

# Run tests and show performance
python3 test_lis.py
```

## Interactive Demo

The demo script showcases various features:

```bash
python3 demo_lis.py
```

This will show examples of all major features and optionally start an interactive session.

## Requirements

- Python 3.10+ (for pattern matching)
- pytest 8.4.1+ (for testing)

Install requirements:
```bash
pip install -r requirements.txt
```

## Dependencies

The project uses minimal dependencies:
- `pytest`: Testing framework with fixtures and advanced features
- No runtime dependencies for the interpreter itself

## Architecture

The interpreter consists of four main components:

1. **Lexer/Tokenizer** (`tokenize`): Converts source code into tokens
2. **Parser** (`parse`, `read_from_tokens`): Builds abstract syntax tree
3. **Environment** (`Env`, `standard_env`): Manages variable scoping
4. **Evaluator** (`eval`): Executes the parsed expressions

