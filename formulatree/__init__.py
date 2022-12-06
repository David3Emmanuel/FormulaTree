from typing import Any
from .nodes import Root
from .preprocessing import preprocess, Token


def compile_expr(expr_input: Any):
    tokens = preprocess(expr_input)
    root = Root()
    for token in tokens:
        if isinstance(token, Token):
            root.add(token.to_node())
        elif isinstance(token, list):
            paren = compile_expr(token)
            root.add(paren)
    return root


def simplify(expression: Root):
    return expression