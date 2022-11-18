from typing import Union, Any
from nodes import *
import re

operations = {
    "+": Add,
    "-": Neg,
    "*": Mult,
    "/": Inv,
    "^": Pow
}
opening_chars = "[(\\{"
closing_chars = "])\\}"
opening_types = {
    "[": Func,
    "{": Set,
    "\\": Const
}


def main():
    expr_str = input("Enter expression: ")
    expression = compile(expr_str)
    print("Expression:", expression)


def string_to_list(expr_str: str) -> list[str]:
    expr_list = []
    current = ''
    level = 0
    for c in expr_str:
        if re.match(r"\s", c):
            continue

        # Check for parentheses
        found_close = False
        for open, close in zip(opening_chars, closing_chars):
            if c == close and current.startswith(open):
                found_close = True
                break
        if found_close:
            if level == 0:
                expr_list.append(current + close)
                current = ''
            else:
                level -= 1
                current += c
        elif c in opening_chars:
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
            elif c in operations:
                expr_list.append(c)
            else:
                raise ValueError(f"Unidentified character '{c}'")

    return expr_list


class Token:
    def __init__(self, content: str, token_type: type):
        self.content = content
        self.type = token_type
    
    def to_node(self):
        return self.type(self.content)

    def __repr__(self):
        return f"({self.content}, {self.type.__name__})"


def list_to_tokens(expr_list: list[str]) -> list[Union[Token, list]]:
    tokens = []
    for term in expr_list:
        if term[0] == '(':
            tokens.append(preprocess(term[1:-1], False))
        elif term[0] in opening_chars:
            assert term[-1] in closing_chars
            tokens.append(Token(term, opening_types[term[0]]))
        elif term in operations:
            tokens.append(Token(term, operations[term]))
        elif re.match(r"^[A-Za-z]$", term):
            tokens.append(Token(term, Var))
        elif re.match(r"\d", term):
            tokens.append(Token(term, Num))
        else:
            raise ValueError(f"Unidentified term '{term}'")
    return tokens


def preprocess(expr_input, root=True) -> list[Union[Token, list]]:
    if isinstance(expr_input, str):
        expr_list = string_to_list(expr_input)
        if root: print("List:", expr_list)
        tokens = list_to_tokens(expr_list)
        if root: print("Tokens:", tokens)
    elif isinstance(expr_input, list):
        return expr_input
    else:
        raise ValueError(f"Cannot process input '{expr_input}'")
    return tokens


def compile(expr_input: Any, root=True):
    tokens = preprocess(expr_input)
    root = Root()
    for token in tokens:
        if isinstance(token, Token):
            root.add(token.to_node())
        elif isinstance(token, list):
            paren = compile(token, False)
            root.add(paren)
    return root


if __name__ == "__main__":
    main()
