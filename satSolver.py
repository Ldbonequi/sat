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
        val = literal_values[int(self.identity.strip("~x")) - 1]
        if "~" in self.identity:
            if val is None:
                return None
            else:
                return not val
        else:
            return val

    def __str__(self) -> str:  # enable printing literals
        return self.identity

    def __repr__(self) -> str:  # properly display literal inside of printed lists
        return self.identity


class expression:
    def __init__(self, expression: str) -> None:
        self.expression: str = expression
        self.clauses: list[list[literal]] = list()
        self.literal_count: int = int()
        self.parseInput(expression)
        self.literal_values: list[bool | None] = [None] * self.literal_count
        self.sat_solutions: list[list[bool | None]] = list()

    def parseInput(self, input: str):
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
            if clause:
                self.clauses.append(clause)
        self.literal_count = len(literals)

        if not self.clauses:
            raise Exception("Unable to parse expression")

    def __str__(self) -> str:
        return self.expression

    def sat(self, expand=False):
        """
        Determines if the expression is sat, adding all satisfying Combinations to self.sat_solutions.
        returns True if expresssion is sat, False otherwise
        params:
            expand - whether to expand dont cares
        """
        any_sat = False

        def backtrack():
            nonlocal any_sat

            local_assigned = list()
            while True:
                assigned = self.unit_propagate()
                if not assigned:
                    break
                local_assigned.extend(assigned)

            eval = self.expression_eval()
            if eval is not None and (
                not expand or None not in self.literal_values
            ):  # prune sat branches to save time if expand is false
                if eval:
                    self.sat_solutions.append(self.literal_values.copy())
                    any_sat = True

                # unassign literals assigned by unit_propagate before returning
                for v in local_assigned:
                    self.assign(v, None)
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

            # unassign literals assigned by unit_propagate before returning
            for v in local_assigned:
                self.assign(v, None)

            self.assign(next, None)

        backtrack()
        return any_sat

    def assign(self, literal: int, value: bool | None):
        """
        Assigns a literal to a boolean value
        params:
            literal: literal number to assign (n assigns xn)
            value: boolean value that literal will be assigned to
        """
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

    def unit_propagate(self) -> list[int]:
        """
        Performs unit propagation:
        if there is a clause with exactly one unassigned literal and no
        satisfied literal, assign that literal to satisfy the clause.
        Returns a list of var_nums of modified literals
        """
        assigned = list()
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
                assigned.append(var_num)
        return assigned

    def print_solutions(self, numbers=True):
        """
        Prints all solutions found by expression.sat()
        params:
            numbers: whether to print solution Numbers
        """
        for idx, sol in enumerate(self.sat_solutions):
            if numbers:
                print(f"  Solution {idx + 1}:")
            for i, v in enumerate(sol):
                print(f"    x{i + 1} = {'DC' if v is None else int(v)}")
            print()

    def merge_solutions(self):
        """
        Repeatedly merges any solution pairs with a single difference in order to find the smallest
        returns smallest solution with the least fixed assignments / max dont cares
        """
        changed = True
        while changed:
            changed = False
            i = 0
            while i < len(self.sat_solutions):
                for j in range(i + 1, len(self.sat_solutions)):
                    diffs = [
                        k
                        for k in range(len(self.sat_solutions[i]))
                        if self.sat_solutions[i][k] != self.sat_solutions[j][k]
                    ]
                    if len(diffs) == 1:
                        self.sat_solutions[i][diffs[0]] = None
                        del self.sat_solutions[j]
                        changed = True
                        break
                if changed:
                    break
                i += 1

        return max(self.sat_solutions, key=lambda s: s.count(None))


def sat_solver(Fixed=False, smallest=False, expand=None, all_solutions=True):
    if expand is None:
        choice = input("Would you like to expand out Dont Cares (y/n):")
        if choice.lower() == "y":
            expand = True
        elif choice.lower() == "n":
            expand = False
        else:
            print("could not parse y or n please try again:")
            main()

    exp = safe_get_expression("Enter Expression: ")
    if Fixed:
        for match in re.findall(
            r"x(\d+)\s*=\s*([01])", input("Fixed variables (e.g. x1=1 x2=0): ")
        ):
            exp.assign(int(match[0]), bool(int(match[1])))
    if exp.sat(expand):
        if all_solutions:
            print(f"{len(exp.sat_solutions)} SAT Combinations:\n")
            exp.print_solutions()

        if smallest:
            exp.sat_solutions = [exp.merge_solutions()]
            print("smallest solution:")
            exp.print_solutions(numbers=False)
    else:
        print("UNSAT")


def compare_functions():
    f1 = safe_get_expression("Function 1: ")
    f2 = safe_get_expression("Function 2: ")
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
        print("NOT EQUIVALENT — differing solutions:")
        for a in diff:
            print({f"x{i + 1}": int(v) for i, v in enumerate(a)})


def prime_implicants():
    exp = safe_get_expression("Enter Expression: ")
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


def safe_get_expression(message) -> expression:
    try:
        exp = expression(input(message).strip())
    except Exception as e:
        print()
        print(f"{e}, please try again:")
        main()
        return
    return exp


def main():
    print("Please Select An Option:")
    print("1) SAT Solver")
    print("2) SAT Solver w/ Fixed Assignments")
    print("3) SAT Solver Smallest Solution")
    print("4) Compare Functions (F1 XOR F2)")
    choice = input("Enter Selection Choice: ").strip()
    if choice == "1":
        sat_solver()
    elif choice == "2":
        sat_solver(Fixed=True)
    elif choice == "3":
        sat_solver(all_solutions=False, smallest=True, expand=False)
    elif choice == "4":
        compare_functions()
    else:
        print()
        print(f"Could Not Parse <{choice}>, please try again.")
        main()
        return


if __name__ == "__main__":
    main()
