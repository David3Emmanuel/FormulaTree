class Node:
    def __init__(self) -> None:
        self.children = []
    
    def __repr__(self) -> str:
        return f"{type(self).__name__}"


class Root(Node):
    def __init__(self) -> None:
        super().__init__()

    def add(self, node):
        self.children.append(node)
    
    def __repr__(self):
        return f"{self.children}"


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
