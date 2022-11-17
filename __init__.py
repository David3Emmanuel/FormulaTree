# from nodes import *

def main():
    expr_str = input("Enter expression: ")
    expression = compile(expr_str)
    print(expression)


def string_to_list(expr_str):
    return []


def list_to_tokens(expr_list):
    return []


def preprocess(expr_input):
    if isinstance(expr_input, str):
        expr_list = string_to_list(expr_input)
        tokens = list_to_tokens(expr_list)
    return tokens


def compile(tokens):
    tokens = preprocess(tokens)
    return None


if __name__ == "__main__":
    main()
