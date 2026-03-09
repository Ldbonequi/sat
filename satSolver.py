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
        self.assigned_literals: int = 0
        self.sat_solutions: list[list[bool | None]] = list()

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
        any_sat = False

        def backtrack():
            nonlocal any_sat
            eval = self.expression_eval()
            if eval is not None:
                if eval:
                    self.sat_solutions.append(self.literal_values.copy())
                    any_sat = True
                return

            next = None
            for i, x in enumerate(self.literal_values):
                if x is None:
                    next = i + 1
                    break

            if next is None:
                return False  # shouldnt happen

            for b in [True, False]:
                self.assign(next, b)
                backtrack()

            self.assign(next, None)

        backtrack()
        return any_sat

    def assign(self, literal: int, value: bool | None):
        idx = literal - 1
        self.literal_values[idx] = value

    def expression_eval(self):
        """
        returns True if all clauses are true
        returns None if any clauses are none
        returns False if no clauses are None and any clause is false
        """
        to_return = True
        for clause in self.clauses:
            eval = self.clause_eval(clause)
            if eval is None:
                return None
            if not eval:
                to_return = False
        return to_return

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
            lit_eval = lit.eval(self.literal_values)
            if lit_eval is None and not to_return:
                to_return = None
            if lit_eval:
                return True
        return to_return

    def print_literal_values(self):
        for i in range(1, self.literal_count + 1):
            print(f"x{i}: {self.literal_values[i - 1]}")


def main():
    exp = expression("(x1 + x2)(x3 + x4)")
    print(f"sat: {exp.sat()}")
    print(f"solutions: {exp.sat_solutions if exp.sat_solutions else 'unsat'}")


if __name__ == "__main__":
    main()
