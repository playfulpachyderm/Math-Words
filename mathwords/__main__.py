from .lexer import *
import sys

# epic REPL
while True:
    try:
        print(">> " + evaluate(input("expr: ")))
    except Exception as e:
        print("({}) {}".format(type(e).__name__, " ".join(e.args)))
