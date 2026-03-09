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
        """
        Determines if the expression is sat, adding all satisfying Combinations to self.sat_solutions.
        returns True if expresssion is sat, False otherwise
        """
        any_sat = False

        def backtrack():
            nonlocal any_sat

            while self.unit_propagate():
                pass  # continue to unit propagate until no changes are made

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

    def unit_propagate(self) -> bool:
        """
        Performs unit propagation:
        if there is a clause with exactly one unassigned literal and no
        satisfied literal, assign that literal to satisfy the clause.
        Returns True if any assignment was made, otherwise False.
        """
        for clause in self.clauses:
            unassigned = []
            satisfied = False
            for lit in clause:
                val = lit.eval(self.literal_values)
                if val is True:
                    satisfied = True
                    break
                if val is None:
                    unassigned.append(lit)
            if satisfied:
                continue
            if len(unassigned) == 1:
                lit = unassigned[0]
                var_num = int(lit.identity.strip("~x"))
                self.assign(var_num, "~" not in lit.identity)
                return True
        return False

    def prime_implicants(self) -> list[tuple]:
        # get all minterms
        n = self.literal_count
        minterms = []
        for mask in range(2**n):
            assignment = tuple((mask >> i) & 1 == 1 for i in range(n))
            self.literal_values = list(assignment)
            if self.expression_eval() is True:
                minterms.append(assignment)
        self.literal_values = [None] * n

        # Merge the pairs
        current = list(dict.fromkeys(minterms))
        primes = []
        while current:
            merged = []
            used = set()
            for i in range(len(current)):
                for j in range(i + 1, len(current)):
                    result = self.merge(current[i], current[j])
                    if result is not None:
                        if result not in merged:
                            merged.append(result)
                        used.add(i)
                        used.add(j)
            for i, imp in enumerate(current):
                if i not in used:
                    primes.append(imp)
            current = list(dict.fromkeys(merged))
        return primes

    def merge(self, a, b):
        diff = [
            i
            for i in range(len(a))
            if a[i] != b[i] and a[i] is not None and b[i] is not None
        ]
        if len(diff) != 1:
            return None
        result = list(a)
        result[diff[0]] = None
        return tuple(result)


def main():
    print("1) SAT Solver")
    print("2) SAT Solver w/ Fixed Assignments")
    print("3) Compare Functions (F1 XOR F2)")
    print("4) Prime Implicants")
    choice = input("Enter Selection Choice: ").strip()

    if choice == "1":
        exp = expression(input("Enter Expression: ").strip())
        exp.sat()
        if not exp.sat_solutions:
            print("UNSAT")
        else:
            print(f"{len(exp.sat_solutions)} SAT Combinations:\n")
            for idx, sol in enumerate(exp.sat_solutions):
                print(f"  Solution {idx + 1}:")
                for i, v in enumerate(sol):
                    print(f"    x{i + 1} = {'DC' if v is None else int(v)}")
                print()

    elif choice == "2":
        exp = expression(input("Enter Expression: ").strip())
        for match in re.findall(
            r"x(\d+)\s*=\s*([01])", input("Fixed variables (e.g. x1=1 x2=0): ")
        ):
            exp.assign(int(match[0]), bool(int(match[1])))
        exp.sat()
        if not exp.sat_solutions:
            print("UNSAT")
        else:
            print(f"{len(exp.sat_solutions)} SAT Combinations:\n")
            for idx, sol in enumerate(exp.sat_solutions):
                print(f"  Solution {idx + 1}:")
                for i, v in enumerate(sol):
                    print(f"    x{i + 1} = {'DC' if v is None else int(v)}")
                print()

    elif choice == "3":
        f1 = expression(input("Function 1: ").strip())
        f2 = expression(input("Function 2: ").strip())
        n = max(f1.literal_count, f2.literal_count)
        diff = []
        for mask in range(2**n):
            assignment = [(mask >> i) & 1 == 1 for i in range(n)]
            f1.literal_values = assignment[: f1.literal_count]
            f2.literal_values = assignment[: f2.literal_count]
            if f1.expression_eval() != f2.expression_eval():
                diff.append(assignment)
        if not diff:
            print("EQUIVALENT")
        else:
            print("NOT EQUIVALENT — differing inputs:")
            for a in diff:
                print({f"x{i + 1}": int(v) for i, v in enumerate(a)})

    elif choice == "4":
        exp = expression(input("Enter Expression: ").strip())
        pis = exp.prime_implicants()
        if not pis:
            print("UNSAT")
        else:
            terms = ", ".join(
                "".join(
                    ("~" if not v else "") + f"x{i + 1}"
                    for i, v in enumerate(pi)
                    if v is not None
                )
                for pi in pis
            )
            print(f"\nPrime Implicants: {terms}")


if __name__ == "__main__":
    main()
