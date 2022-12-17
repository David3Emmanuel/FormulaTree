from typing import Self


class Node:
    def __init__(self) -> None:
        self.children = []
        self.parent = None
        self.name = type(self).__name__
        self.size = 0

    def eval(self) -> Self:
        raise NotImplementedError()

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

    def __eq__(self, other):
        raise NotImplementedError()
    
    def str(self) -> str:
        return self.__repr__()


class Root(Node):
    def __init__(self) -> None:
        super().__init__()
        self.current = self
        self.size = 1
        self.main = True

    def eval(self) -> Node:
        return self.children[0].eval()

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
    def __init__(self, content='*') -> None:
        super().__init__()
        self.size = 2

    def eval(self) -> Node:
        coeff_dict = self.get_coeffs()
        terms = []
        for variables, coeff in coeff_dict.values():
            term = Mult()
            term.add(Num(coeff))
            for var in variables:
                term.add(var)
            terms.append(term.eval())

        if len(terms) == 1:
            return terms[0]
        else:
            output = Add()
            for term in terms:
                output.add(term)
            return output

    def get_coeffs(self):
        coeff_dict = {}

        def add_coeff(coeff, variables: list):
            if coeff is None:
                coeff = 1
            var_str = repr(sorted(variables))
            if var_str in coeff_dict:
                coeff_dict[var_str][1] += coeff
            else:
                coeff_dict[var_str] = [variables, coeff]
                return

        for term_ in self.children:
            term = term_.eval()
            if isinstance(term, Num):
                add_coeff(term.value, [])
            elif isinstance(term, Var):
                add_coeff(1, [term])
            elif isinstance(term, Mult):
                factors = term.factors()
                coefficient, variables = None, []
                for factor in factors:
                    if isinstance(factor, Num):
                        assert coefficient is None
                        coefficient = factor.value
                    else:
                        variables.append(factor)
                add_coeff(coefficient, variables)
                
            else:
                raise ValueError(f"Unrecognized term {term}")

        return coeff_dict

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow, Mult, Inv, Neg))

    def __eq__(self, other):
        return isinstance(other, Add)
    
    def str(self):
        output = ' + '.join([term.str() for term in self.children])
        return output.replace('+ -', '- ')


class Neg(Node):
    def __init__(self, content='-') -> None:
        super().__init__()
        self.size = 1
    
    def eval(self):
        output = Mult()
        output.add(Num(-1))
        output.add(self.children[0])
        return output.eval()

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow, Mult, Inv, Neg))

    def __eq__(self, other):
        return False

class Mult(Node):
    def __init__(self, content='*') -> None:
        super().__init__()
        self.size = 2
    
    def factors(self) -> list[Node]:
        output = []
        for child in [child.eval() for child in self.children]:
            if isinstance(child, (Num, Var)):
                output.append(child)
            elif isinstance(child, (Mult, Pow)):
                output.extend(child.factors())
            else:
                raise ValueError(f"Cannot find the factors of {child}")
        return output
    
    def eval(self) -> Node:
        coefficient = 1
        counts = {}

        for factor in self.factors():
            if isinstance(factor, Num):
                coefficient *= factor.value
            else:
                factor_str = repr(factor)
                if factor_str in counts:
                    counts[factor_str][1] += 1
                else:
                    counts[factor_str] = [factor, 1]

        if len(counts) == 0:
            return Num(coefficient)
        
        output = Mult()
        if coefficient != 1:
            output.add(Num(coefficient))
        for factor, count in counts.values():
            if count == 1:
                output.add(factor)
            else:
                new_factor = Pow()
                new_factor.add(factor)
                new_factor.add(Num(count))
                output.add(new_factor)
                
        return output

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow))

    def __eq__(self, other):
        return isinstance(other, (Mult, Inv))
    
    def str(self):
        def format_factor(factor):
            if isinstance(factor, Num):
                if factor.value == 1:
                    return ''
                elif factor.value == -1:
                    return '-'
            return factor.str()
        return ''.join([format_factor(factor) for factor in self.children])


class Inv(Node):
    def __init__(self, content='/') -> None:
        super().__init__()
        self.size = 1

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func, Pow))

    def __eq__(self, other):
        return isinstance(other, (Mult, Inv))


class Pow(Node):
    def __init__(self, content='^') -> None:
        super().__init__()
        self.size = 2

    def factors(self) -> list[Node]:
        base, exponent = self.children
        if isinstance(exponent, Num):
            if isinstance(exponent.value, int):
                return [base for i in range(exponent.value)]
        return [self]

    def __gt__(self, other):
        if isinstance(other, Root):
            return not other.main
        return isinstance(other, (Num, Const, Var, Func))

    def __eq__(self, other):
        return isinstance(other, Pow)
    
    def str(self):
        return self.children[0].str() + '^' + self.children[1].str()


class Num(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.name = str(content)

        val = float(content)
        if int(val) == val:
            self.value = int(val)
        else:
            self.value = val

    def eval(self) -> Self:
        return self

    def __gt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, (Num, Const, Var))
    
    def str(self):
        return self.name


class Var(Node):
    def __init__(self, content) -> None:
        super().__init__()
        self.name = content
    
    def eval(self):
        return self

    def __gt__(self, other):
        return False

    def __eq__(self, other):
        return isinstance(other, (Num, Const, Var))
    
    def str(self):
        return self.name


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
