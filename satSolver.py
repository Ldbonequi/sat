import re


class literal:
    def __init__(self, identity: str) -> None:
        self.identity: str = identity

    def eval(self, literal_values: list[bool | None]):
        """
        returns the value of the literal as True,False,None
        params:
            literal_values: list of literal_values (xn) at index n-1
        """
        # return opposite of value if value has not
        if "~" in self.identity:
            val = literal_values[int(self.identity[2]) - 1]
            if val:
                return False
            elif val is None:
                return None
            elif not val:
                return True
        else:
            return literal_values[int(self.identity[1]) - 1]

    def __str__(self) -> str:  # enable printing literals
        return self.identity

    def __repr__(self) -> str:  # properly display literal inside of printed lists
        return self.identity


class expression:
    def __init__(self, expression: str) -> None:
        self.expression: str = expression
        self.clauses: list[list[literal]] = list()
        self.literal_count: int = int()
        self.__parseInput__(expression)
        self.literal_values: list[bool | None] = [None] * self.literal_count

    def __parseInput__(self, input: str):
        """
        takes a cnf expression and populates sefl.literal_count and self.clauses
        params:
            input: cnf expression as string
        """
        literals: set = set()
        input = input.strip(" +(")  # remove useless chars
        clause_strs = [c for c in re.split(r"[.)]", input) if c]  # split clauses
        for c in clause_strs:
            clause = list()
            for item in re.findall(r"~?x\d+", c):  # find all literals
                clause.append(literal(item))
                literals.add(item.strip("~"))
            self.clauses.append(clause)
        self.literal_count = len(literals)

    def __str__(self) -> str:
        return self.expression

    def sat(self):
        pass  # TODO create basic exhaustive search

    def assign(self, literal: str, value: bool | None):
        idx = int(literal.strip("x")) - 1
        self.literal_values[idx] = value

    def clause_eval(self, clause: list[literal]):
        """
        returns True if the clause is satisfied
        returns False if the clause is unsat
        returns None if the clause is undetermined
        params:
            clause: clause to evaluate
        """
        to_return = False
        for lit in clause:
            lit = lit.eval(self.literal_values)
            if lit is None and not to_return:
                to_return = None
            if lit:
                return True
        return to_return

    def print_literal_values(self):
        for i in range(1, self.literal_count + 1):
            print(f"x{i}: {self.literal_values[i - 1]}")


def main():
    exp = expression("(~x1 + x2).(x3 + ~x4) x1")
    exp.assign("x1", True)
    exp.assign("x2", True)
    exp.print_literal_values()
    print([exp.clause_eval(clause) for clause in exp.clauses])


if __name__ == "__main__":
    main()
