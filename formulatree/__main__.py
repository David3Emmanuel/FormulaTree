from . import compile_expr

def main():
    expr_str = input("Enter expression: ")
    expression = compile_expr(expr_str)
    print("Expression:", expression)


if __name__ == "__main__":
    main()