"""
Test suite for the Lispy Scheme interpreter using pytest.
Tests various features including arithmetic, variables, functions, conditionals, and more.
"""

import sys
import os
import pytest

# Add the current directory to sys.path so we can import lis
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import lis


@pytest.fixture
def env():
    """Fixture that provides a fresh environment for each test."""
    return lis.standard_env()


def lisp_eval(expression: str, env):
    """Helper function to parse and evaluate a Lisp expression."""
    return lis.eval(lis.parse(expression), env)


def test_basic_arithmetic(env):
    """Test basic arithmetic operations."""
    assert lisp_eval("(+ 2 3)", env) == 5
    assert lisp_eval("(- 10 4)", env) == 6
    assert lisp_eval("(* 4 5)", env) == 20
    assert lisp_eval("(/ 15 3)", env) == 5.0


def test_nested_arithmetic(env):
    """Test nested arithmetic expressions."""
    assert lisp_eval("(+ (* 2 3) (- 8 3))", env) == 11
    assert lisp_eval("(- (* 4 5) (+ 2 3))", env) == 15
    assert lisp_eval("(/ (+ 10 5) (- 8 5))", env) == 5.0


def test_comparison_operators(env):
    """Test comparison operations."""
    assert lisp_eval("(> 5 3)", env) is True
    assert lisp_eval("(< 5 3)", env) is False
    assert lisp_eval("(>= 5 5)", env) is True
    assert lisp_eval("(<= 3 5)", env) is True
    assert lisp_eval("(= 5 5)", env) is True
    assert lisp_eval("(= 5 3)", env) is False


def test_constants(env):
    """Test number and symbol constants."""
    assert lisp_eval("42", env) == 42
    assert lisp_eval("3.14", env) == 3.14
    assert lisp_eval("-5", env) == -5


def test_quote(env):
    """Test quote expressions."""
    assert lisp_eval("(quote hello)", env) == "hello"
    assert lisp_eval("(quote (1 2 3))", env) == [1, 2, 3]
    assert lisp_eval("(quote (+ 1 2))", env) == ["+", 1, 2]


def test_variables(env):
    """Test variable definition and access."""
    lisp_eval("(define x 10)", env)
    assert lisp_eval("x", env) == 10

    lisp_eval("(define y (* x 2))", env)
    assert lisp_eval("y", env) == 20


def test_variable_assignment(env):
    """Test variable reassignment with set!."""
    lisp_eval("(define x 5)", env)
    assert lisp_eval("x", env) == 5

    lisp_eval("(set! x 10)", env)
    assert lisp_eval("x", env) == 10


def test_conditionals(env):
    """Test if expressions."""
    assert lisp_eval("(if (> 5 3) (quote yes) (quote no))", env) == "yes"
    assert lisp_eval("(if (< 5 3) (quote yes) (quote no))", env) == "no"
    assert lisp_eval("(if (= 2 2) (+ 1 1) (* 3 3))", env) == 2


def test_lambda_functions(env):
    """Test lambda function creation and invocation."""
    # Simple lambda
    lisp_eval("(define square (lambda (x) (* x x)))", env)
    assert lisp_eval("(square 5)", env) == 25

    # Lambda with multiple parameters
    lisp_eval("(define add (lambda (x y) (+ x y)))", env)
    assert lisp_eval("(add 3 4)", env) == 7

    # Direct lambda invocation
    assert lisp_eval("((lambda (x) (* x 2)) 6)", env) == 12


def test_recursive_functions(env):
    """Test recursive function definitions."""
    # Factorial function
    lisp_eval(
        """
        (define fact 
            (lambda (n) 
                (if (<= n 1) 
                    1 
                    (* n (fact (- n 1))))))
    """,
        env,
    )
    assert lisp_eval("(fact 5)", env) == 120
    assert lisp_eval("(fact 0)", env) == 1

    # Fibonacci function
    lisp_eval(
        """
        (define fib 
            (lambda (n) 
                (if (<= n 1) 
                    n 
                    (+ (fib (- n 1)) (fib (- n 2))))))
    """,
        env,
    )
    assert lisp_eval("(fib 6)", env) == 8


def test_list_operations(env):
    """Test list manipulation functions."""
    # car (first element)
    assert lisp_eval("(car (quote (1 2 3)))", env) == 1

    # cdr (rest of list)
    assert lisp_eval("(cdr (quote (1 2 3)))", env) == [2, 3]

    # cons (construct list)
    assert lisp_eval("(cons 1 (quote (2 3)))", env) == [1, 2, 3]

    # list construction
    assert lisp_eval("(list 1 2 3)", env) == [1, 2, 3]

    # length
    assert lisp_eval("(length (quote (1 2 3 4)))", env) == 4

    # append
    assert lisp_eval("(append (quote (1 2)) (quote (3 4)))", env) == [1, 2, 3, 4]


def test_predicates(env):
    """Test predicate functions."""
    # number?
    assert lisp_eval("(number? 42)", env) is True
    assert lisp_eval("(number? (quote hello))", env) is False

    # symbol?
    assert lisp_eval("(symbol? (quote hello))", env) is True
    assert lisp_eval("(symbol? 42)", env) is False

    # list?
    assert lisp_eval("(list? (quote (1 2 3)))", env) is True
    assert lisp_eval("(list? 42)", env) is False

    # null?
    assert lisp_eval("(null? (quote ()))", env) is True
    assert lisp_eval("(null? (quote (1)))", env) is False

    # procedure?
    lisp_eval("(define f (lambda (x) x))", env)
    assert lisp_eval("(procedure? f)", env) is True
    assert lisp_eval("(procedure? 42)", env) is False


def test_math_functions(env):
    """Test mathematical functions from the math module."""
    # abs
    assert lisp_eval("(abs -5)", env) == 5
    assert lisp_eval("(abs 3)", env) == 3

    # max and min
    assert lisp_eval("(max 1 5 3 2)", env) == 5
    assert lisp_eval("(min 1 5 3 2)", env) == 1

    # round
    assert lisp_eval("(round 3.7)", env) == 4
    assert lisp_eval("(round 3.2)", env) == 3


def test_begin(env):
    """Test begin expressions (sequence evaluation)."""
    result = lisp_eval(
        """
        (begin 
            (define x 1)
            (set! x (+ x 1))
            (set! x (* x 2))
            x)
    """,
        env,
    )
    assert result == 4


def test_apply_function(env):
    """Test the apply function."""
    assert lisp_eval("(apply + (quote (1 2 3 4)))", env) == 10
    assert lisp_eval("(apply * (quote (2 3 4)))", env) == 24


def test_map_function(env):
    """Test the map function."""
    lisp_eval("(define square (lambda (x) (* x x)))", env)
    result = list(lisp_eval("(map square (quote (1 2 3 4)))", env))
    assert result == [1, 4, 9, 16]


def test_complex_expressions(env):
    """Test more complex expressions combining multiple features."""
    # Define a function that uses conditionals and recursion
    lisp_eval(
        """
        (define sum-range 
            (lambda (start end) 
                (if (> start end) 
                    0 
                    (+ start (sum-range (+ start 1) end)))))
    """,
        env,
    )
    assert lisp_eval("(sum-range 1 5)", env) == 15  # 1+2+3+4+5

    # Define a function using list operations
    lisp_eval(
        """
        (define reverse-list 
            (lambda (lst) 
                (if (null? lst) 
                    (quote ()) 
                    (append (reverse-list (cdr lst)) (list (car lst))))))
    """,
        env,
    )
    result = lisp_eval("(reverse-list (quote (1 2 3 4)))", env)
    assert result == [4, 3, 2, 1]


def test_error_handling(env):
    """Test that errors are properly raised."""
    # Undefined variable
    with pytest.raises(NameError):
        lisp_eval("undefined_variable", env)

    # Division by zero
    with pytest.raises(ZeroDivisionError):
        lisp_eval("(/ 5 0)", env)

    # Syntax error
    with pytest.raises(SyntaxError):
        lis.parse("(+ 1 2")  # Missing closing parenthesis


def test_parsing():
    """Test the parsing functionality."""
    # Test tokenization
    tokens = lis.tokenize("(+ 1 2)")
    assert tokens == ["(", "+", "1", "2", ")"]

    # Test parsing
    parsed = lis.parse("(+ 1 2)")
    assert parsed == ["+", 1, 2]

    # Test atom parsing
    assert lis.atom("42") == 42
    assert lis.atom("3.14") == 3.14
    assert lis.atom("hello") == "hello"


def test_lispstr():
    """Test the Lisp string representation function."""
    assert lis.lispstr(42) == "42"
    assert lis.lispstr("hello") == "hello"
    assert lis.lispstr([1, 2, 3]) == "(1 2 3)"
    assert lis.lispstr(["+", 1, 2]) == "(+ 1 2)"


def run_performance_tests():
    """Run some performance tests to ensure the interpreter is reasonably fast."""
    import time

    print("\n" + "=" * 50)
    print("PERFORMANCE TESTS")
    print("=" * 50)

    env = lis.standard_env()

    # Test recursive factorial performance
    lis.eval(
        lis.parse("""
        (define fact 
            (lambda (n) 
                (if (<= n 1) 
                    1 
                    (* n (fact (- n 1))))))
    """),
        env,
    )

    start_time = time.time()
    result = lis.eval(lis.parse("(fact 10)"), env)
    end_time = time.time()

    print(f"Factorial of 10: {result}")
    print(f"Time taken: {(end_time - start_time) * 1000:.2f} ms")

    # Test Fibonacci performance
    lis.eval(
        lis.parse("""
        (define fib 
            (lambda (n) 
                (if (<= n 1) 
                    n 
                    (+ (fib (- n 1)) (fib (- n 2))))))
    """),
        env,
    )

    start_time = time.time()
    result = lis.eval(lis.parse("(fib 20)"), env)
    end_time = time.time()

    print(f"Fibonacci of 20: {result}")
    print(f"Time taken: {(end_time - start_time) * 1000:.2f} ms")
