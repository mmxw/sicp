################
# Lispy: Scheme Interpreter in Python
# Based on the original Lispy by Peter Norvig
# https://norvig.com/lispy.html
################


import math
import operator as op
from typing import Any

################ Types

Symbol = str  # A Lisp Symbol is implemented as a Python str
List = list  # A Lisp List is implemented as a Python list
Number = int | float  # A Lisp Number is implemented as a Python int or float

################ Parsing: parse, tokenize, and read_from_tokens


def parse(program: str) -> Any:
    "Read a Scheme expression from a string."
    return read_from_tokens(tokenize(program))


def tokenize(s: str) -> list[str]:
    "Convert a string into a list of tokens."
    return s.replace("(", " ( ").replace(")", " ) ").split()


def read_from_tokens(tokens: list[str]) -> Any:
    "Read an expression from a sequence of tokens."
    if len(tokens) == 0:
        raise SyntaxError("unexpected EOF while reading")
    token = tokens.pop(0)
    if "(" == token:
        L = []
        while len(tokens) > 0 and tokens[0] != ")":
            L.append(read_from_tokens(tokens))
        if len(tokens) == 0:
            raise SyntaxError(
                "unexpected EOF while reading - missing closing parenthesis"
            )
        tokens.pop(0)  # pop off ')'
        return L
    elif ")" == token:
        raise SyntaxError("unexpected )")
    else:
        return atom(token)


def atom(token: str) -> Symbol | Number:
    "Numbers become numbers; every other token is a symbol."
    try:
        return int(token)
    except ValueError:
        try:
            return float(token)
        except ValueError:
            return Symbol(token)


################ Environments


def standard_env() -> "Env":
    "An environment with some Scheme standard procedures."

    def scheme_apply(proc, args):
        """Apply a procedure to a list of arguments."""
        if callable(proc):
            return proc(*args)
        else:
            raise TypeError(f"'{proc}' is not callable")

    def variadic_add(*args):
        """Addition that accepts multiple arguments."""
        return sum(args)

    def variadic_mul(*args):
        """Multiplication that accepts multiple arguments."""
        result = 1
        for x in args:
            result *= x
        return result

    env = Env()
    env.update(vars(math))  # sin, cos, sqrt, pi, ...
    env.update(
        {
            "+": variadic_add,
            "-": op.sub,
            "*": variadic_mul,
            "/": op.truediv,
            ">": op.gt,
            "<": op.lt,
            ">=": op.ge,
            "<=": op.le,
            "=": op.eq,
            "abs": abs,
            "append": op.add,
            "apply": scheme_apply,
            "begin": lambda *x: x[-1],
            "car": lambda x: x[0],
            "cdr": lambda x: x[1:],
            "cons": lambda x, y: [x] + y,
            "eq?": op.is_,
            "equal?": op.eq,
            "length": len,
            "list": lambda *x: list(x),
            "list?": lambda x: isinstance(x, list),
            "map": map,
            "max": max,
            "min": min,
            "not": op.not_,
            "null?": lambda x: x == [],
            "number?": lambda x: isinstance(x, Number),
            "procedure?": callable,
            "round": round,
            "symbol?": lambda x: isinstance(x, Symbol),
        }
    )
    return env


class Env(dict):
    "An environment: a dict of {'var':val} pairs, with an outer Env."

    def __init__(self, parms=(), args=(), outer: "Env | None" = None):
        self.update(zip(parms, args))
        self.outer = outer

    def find(self, var: str) -> "Env":
        "Find the innermost Env where var appears."
        if var in self:
            return self
        elif self.outer is not None:
            return self.outer.find(var)
        else:
            raise NameError(f"Variable '{var}' not found")


global_env = standard_env()

################ Interaction: A REPL


def repl(prompt: str = "lis.py >>> ") -> None:
    "A prompt-read-eval-print loop."
    print("Lispy: A Scheme Interpreter in Python")
    print("Based on Peter Norvig's Lispy (https://norvig.com/lispy.html)")
    print("Type expressions like: (+ 1 2), (define x 10), (lambda (x) (* x x))")
    print("Press Ctrl+C or Ctrl+D to exit")
    print("-" * 50)
    
    while True:
        try:
            val = eval(parse(input(prompt)))
            if val is not None:
                print(lispstr(val))
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            print("\nExiting...")
            break
        except (SyntaxError, NameError, ZeroDivisionError) as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")


def lispstr(exp: Any) -> str:
    "Convert a Python object back into a Lisp-readable string."
    if isinstance(exp, List):
        return "(" + " ".join(map(lispstr, exp)) + ")"
    else:
        return str(exp)


################ Procedures


class Procedure:
    "A user-defined Scheme procedure."

    def __init__(self, parms: list, body: list, env: Env):
        self.parms = parms
        self.body = body
        self.env = env

    def __call__(self, *args):
        return eval(self.body, Env(self.parms, args, self.env))


################ eval


def eval(x: Any, env: Env = global_env) -> Any:
    "Evaluate an expression in an environment."
    if isinstance(x, Symbol):  # variable reference
        return env.find(x)[x]
    elif not isinstance(x, List):  # constant literal
        return x
    else:  # list expression
        match x[0]:
            case "quote":  # (quote exp)
                _, exp = x
                return exp
            case "if":  # (if test conseq alt)
                _, test, conseq, alt = x
                exp = conseq if eval(test, env) else alt
                return eval(exp, env)
            case "define":  # (define var exp)
                _, var, exp = x
                env[var] = eval(exp, env)
            case "set!":  # (set! var exp)
                _, var, exp = x
                env.find(var)[var] = eval(exp, env)
            case "lambda":  # (lambda (var...) body)
                _, parms, body = x
                return Procedure(parms, body, env)
            case _:  # (proc arg...)
                proc = eval(x[0], env)
                args = [eval(exp, env) for exp in x[1:]]
                return proc(*args)


################ Main execution

if __name__ == "__main__":
    # Only launch the REPL when run lis.py directly
    repl()
