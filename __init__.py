from nodes import *
import re


def main():
    expr_str = input("Enter expression: ")
    expression = compile(expr_str)
    print(expression)


def string_to_list(expr_str):
    expr_list = []
    current = ''
    level = 0
    for c in expr_str:
        if re.match(r"\s", c):
            continue

        # Check for parentheses
        found_close = False
        for open, close in zip("[(\\{", "])\\}"):
            if c == close and current.startswith(open):
                found_close = True
                break
        if found_close:
            if level == 0:
                expr_list.append(current + close)
                current = ''
            else:
                level -= 1
        elif c in "[(\\{":
            if current:
                current += c
                if current.startswith(c):
                    level += 1
            else:
                current = c
        elif current:
            current += c

        else:
            if re.match(r"[\d\.]", c):
                if expr_list:
                    if re.match(r"[\d\.]", expr_list[-1]):
                        expr_list[-1] += c
                    else:
                        expr_list.append(c)
                else:
                    expr_list.append(c)
            elif re.match(r"[A-Za-z]", c):
                expr_list.append(c)
            elif c in "+-*/^":
                expr_list.append(c)
            else:
                raise ValueError(f"Unidentified character '{c}'")

    return expr_list


def list_to_tokens(expr_list):
    return expr_list


def preprocess(expr_input):
    if isinstance(expr_input, str):
        expr_list = string_to_list(expr_input)
        print(expr_list)
        tokens = list_to_tokens(expr_list)
        print(tokens)
    return tokens


def compile(tokens):
    tokens = preprocess(tokens)
    return tokens


if __name__ == "__main__":
    main()
