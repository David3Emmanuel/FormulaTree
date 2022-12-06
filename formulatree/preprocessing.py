import re
from typing import Union, Any
from .nodes import *


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

    def is_term(token: Union[Token, list]) -> bool:
        if isinstance(token, list):
            return True
        return token.type in [Num, Const, Var]

    def add(token: Union[Token, list]) -> None:
        if tokens:
            if is_term(tokens[-1]):
                if is_term(token) or token.type is Func:
                    tokens.append(Token("*", Mult))
                elif token.type is Neg:
                    tokens.append(Token("+", Add))
                elif token.type is Inv:
                    tokens.append(Token("*", Mult))
        tokens.append(token)

    for term in expr_list:
        if term[0] == '(':
            add(preprocess(term[1:-1], False))
        elif term[0] in opening_chars:
            assert term[-1] in closing_chars
            add(Token(term, opening_types[term[0]]))
        elif term in operations:
            add(Token(term, operations[term]))
        elif re.match(r"^[A-Za-z]$", term):
            add(Token(term, Var))
        elif re.match(r"\d", term):
            add(Token(term, Num))
        else:
            raise ValueError(f"Unidentified term '{term}'")
    return tokens


def preprocess(expr_input, root=True) -> list[Union[Token, list]]:
    if isinstance(expr_input, str):
        expr_list = string_to_list(expr_input)
        if root:
            print("List:", expr_list)
        tokens = list_to_tokens(expr_list)
        if root:
            print("Tokens:", tokens)
    elif isinstance(expr_input, list):
        return expr_input
    else:
        raise ValueError(f"Cannot process input '{expr_input}'")
    return tokens