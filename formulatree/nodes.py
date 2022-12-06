class Node:
    def __init__(self) -> None:
        self.children = []
        self.parent = None
        self.name = type(self).__name__
        self.size = 0

    def add(self, node):
        self.children.append(node)
        node.parent = self

    def full(self) -> bool:
        assert len(self.children) <= self.size, "Overflow"
        return len(self.children) == self.size

    def lineage(self):
        if self.parent:
            return [self] + self.parent.lineage()
        return [self]

    def __repr__(self, level=0) -> str:
        if len(self.children) == 0:
            return f"{self.name}"
        elif len(self.children) == 1:
            return f"{self.name}({self.children[0]})"
        else:
            indent = "\n  "+"  "*level
            e = indent.join([node.__repr__(level+1) for node in self.children])
            return f"{self.name}({indent}{e}\n)"

    def __gt__(self, other):
        raise NotImplementedError()
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()


class Root(Node):
    def __init__(self) -> None:
        super().__init__()
        self.current = self
        self.size = 1
        self.main = True

    def add(self, node):
        if isinstance(node, Root):
            node.main = False
        for parent in self.current.lineage():
            if node > parent:
                continue
            if isinstance(node, (Add, Mult)) and type(node) is type(parent):
                parent.size += 1
                break
            if parent.full():
                if node.full():
                    continue
                else:
                    branch = parent.children.pop()
                    node.add(branch)

            self.current = node
            if parent is self:
                super().add(node)
            else:
                parent.add(node)
            break

    def __gt__(self, other):
        if self.main:
            return True
        else:
            return isinstance(other, (Num, Const, Var))

    def __eq__(self, other):
        if self.main:
            return False
        else:
            if isinstance(other, Root):
                return not other.main
            return False


class Add(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.size = 2

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow, Mult, Inv))

    def __eq__(self, other):
        return isinstance(other, (Add, Neg))


class Neg(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.size = 1

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow, Mult, Inv))

    def __eq__(self, other):
        return isinstance(other, (Add, Neg))


class Mult(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.size = 2

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow))

    def __eq__(self, other):
        return isinstance(other, (Mult, Inv))


class Inv(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.size = 1

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow))

    def __eq__(self, other):
        return isinstance(other, (Mult, Inv))


class Pow(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.size = 2

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func))

    def __eq__(self, other):
        return isinstance(other, Pow)


class Num(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.name = content

    def __gt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, (Num, Const, Var))


class Var(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.name = content

    def __gt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, (Num, Const, Var))


class Func(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.name = content
        self.size = 1

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var))

    def __eq__(self, other):
        return isinstance(other, Func)


class Set(Node):
    def __init__(self, content) -> None:
        super().__init__()


class Const(Node):
    def __init__(self, content) -> None:
        super().__init__()

    def __gt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, (Num, Const, Var))
