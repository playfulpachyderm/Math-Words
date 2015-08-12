from .lexer import *
import sys
while True:
    try:
        print(">> " + unparse(evaluate(input("expr: "))))
    except Exception as e:
        print("({}) {}".format(type(e).__name__, " ".join(e.args)))
