class Node:
    pass


class Root(Node):
    def __init__(self) -> None:
        super().__init__()
    def add(self, token):
        pass


class Add(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Neg(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Mult(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Inv(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Pow(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Num(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Var(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Func(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Set(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Const(Node):
    def __init__(self, content) -> None:
        super().__init__()
