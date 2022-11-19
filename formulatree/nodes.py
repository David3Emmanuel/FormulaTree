class Node:
    def __init__(self) -> None:
        self.children = []
        self.parent = 0
        self.name = type(self).__name__
    
    def add(self, node):
        self.children.append(node)
        node.parent = None
    
    def lineage(self):
        if self.parent:
            return [self] + self.parent.lineage()
        return [self]
    
    def __repr__(self) -> str:
        if len(self.children) == 0:
            return f"{self.name}"
        elif len(self.children) == 1:
            return f"{self.name}({self.children[0]})"
        else:
            e = "\n".join(self.children)
            return f"{self.name}(\n{e}\n)"


class Root(Node):
    def __init__(self) -> None:
        super().__init__()
        self.current = self

    def add(self, node):
        for parent in self.current.lineage():
            if parent is self:
                super().add(node)
            else:
                parent.add(node)
            break
    
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
        self.name = content


class Var(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.name = content


class Func(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.name = content


class Set(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Const(Node):
    def __init__(self, content) -> None:
        super().__init__()
