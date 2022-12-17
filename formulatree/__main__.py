from . import compile_expr, simplify


def main():
    while True:
        expr_str = input("Enter expression: ")
        if not expr_str:
            return
        try:
            expression = compile_expr(expr_str)
            simplified = simplify(expression)
            print("Simplified:", simplified.str())
        except ValueError as error:
            print(error)


if __name__ == "__main__":
    main()