#!/usr/bin/env python3
"""
Demo script for the Lispy Scheme interpreter.
Shows various examples of what the interpreter can do.
"""

import lis


def demo_examples():
    """Run various demo examples to showcase the interpreter."""
    print("🚀 Lispy Scheme Interpreter Demo")
    print("=" * 50)

    examples = [
        # Basic arithmetic
        (
            "Basic Arithmetic",
            ["(+ 2 3 4)", "(* 5 6)", "(- 20 5)", "(/ 15 3)", "(+ (* 2 3) (- 8 2))"],
        ),
        # Variables and definitions
        (
            "Variables & Definitions",
            [
                "(define pi 3.14159)",
                "(define radius 5)",
                "(* pi (* radius radius))",  # Area of circle
            ],
        ),
        # Functions and lambdas
        (
            "Functions & Lambdas",
            [
                "(define square (lambda (x) (* x x)))",
                "(square 7)",
                "(define add-three (lambda (x y z) (+ x y z)))",
                "(add-three 1 2 3)",
                "((lambda (x) (* x 2)) 21)",  # Anonymous function
            ],
        ),
        # Conditionals
        (
            "Conditionals",
            [
                "(define max-of-two (lambda (a b) (if (> a b) a b)))",
                "(max-of-two 10 5)",
                "(max-of-two 3 8)",
            ],
        ),
        # Recursion
        (
            "Recursion",
            [
                "(define factorial (lambda (n) (if (<= n 1) 1 (* n (factorial (- n 1))))))",
                "(factorial 5)",
                "(factorial 6)",
            ],
        ),
        # List operations
        (
            "List Operations",
            [
                "(define my-list (quote (1 2 3 4 5)))",
                "(car my-list)",
                "(cdr my-list)",
                "(cons 0 my-list)",
                "(length my-list)",
            ],
        ),
        # Higher-order functions
        (
            "Higher-Order Functions",
            [
                "(define double (lambda (x) (* x 2)))",
                "(define numbers (quote (1 2 3 4)))",
                "(map double numbers)",
                "(apply + numbers)",
            ],
        ),
        # More complex examples
        (
            "Complex Examples",
            [
                "(define sum-of-squares (lambda (a b) (+ (* a a) (* b b))))",
                "(sum-of-squares 3 4)",
                "(define range-sum (lambda (start end) (if (> start end) 0 (+ start (range-sum (+ start 1) end)))))",
                "(range-sum 1 10)",
            ],
        ),
    ]

    env = lis.standard_env()

    for category, expressions in examples:
        print(f"\n📁 {category}")
        print("-" * len(category))

        for expr in expressions:
            try:
                result = lis.eval(lis.parse(expr), env)
                if result is not None:
                    print(f"  {expr:40} => {lis.lispstr(result)}")
                else:
                    print(f"  {expr:40} => ✓")
            except Exception as e:
                print(f"  {expr:40} => Error: {e}")

    print("\n🎉 Demo completed!")


def interactive_demo():
    """Run an interactive demo where users can input expressions."""
    print("\n🎮 Interactive Mode")
    print("=" * 50)
    print("Enter Lisp expressions (or 'quit' to exit):")
    print("Examples: (+ 1 2), (define x 10), (lambda (x) (* x x))")
    print()

    env = lis.standard_env()

    while True:
        try:
            user_input = input("lispy> ").strip()
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye! 👋")
                break

            if user_input:
                result = lis.eval(lis.parse(user_input), env)
                if result is not None:
                    print(f"=> {lis.lispstr(result)}")

        except KeyboardInterrupt:
            print("\nGoodbye! 👋")
            break
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    # Run the demo examples
    demo_examples()

    # Ask if user wants interactive mode
    print("\n" + "=" * 50)
    try:
        choice = (
            input("Would you like to try interactive mode? (y/n): ").strip().lower()
        )
        if choice in ["y", "yes"]:
            interactive_demo()
    except KeyboardInterrupt:
        print("\nGoodbye! 👋")
