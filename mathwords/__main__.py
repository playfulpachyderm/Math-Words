from .lexer import *
import sys
while True:
    try:
        print(">> " + unparse(evaluate(input("expr: "))))
    except Exception as e:
    	print("(error) {}".format(" ".join(e.args)))
