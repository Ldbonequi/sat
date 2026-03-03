import re


class literal:
    def __init__(self, identity: str) -> None:
        self.identity: str = identity

    def eval(self, literal_values: list[bool]):
        """
        returns the value of the literal
        params:
            literal_values: list of literal_values (xn) at index n
        """
        # return opposite of value if value has not
        if "~" in self.identity:
            val = literal_values[int(self.identity[2])]
            return False if val else True
        else:
            return literal_values[int(self.identity[1])]

    def __str__(self) -> str:  # enable printing literals
        return self.identity

    def __repr__(self) -> str:  # properly display literal inside of printed lists
        return self.identity


def parseInput(input: str):
    """
    takes a cnf expression and returns a count of the literals and a list of clauses
    params:
        input: cnf expression as string
    """
    clauses: list[list[literal]] = list()
    literals: set = set()

    input = input.strip(" +(")  # remove useless chars
    clause_strs = [c for c in re.split(r"[.)]", input) if c]  # split clauses
    for c in clause_strs:
        clause = list()
        for item in re.findall(r"~?x\d+", c):  # find all literals
            clause.append(literal(item))
            literals.add(item.strip("~"))
        clauses.append(clause)

    return len(literals), clauses


def main():
    literal_count: int
    clauses: list[list[literal]]
    literal_count, clauses = parseInput("(~x1 + x2).(x3 + ~x4) x1")
    print(f"terms: {clauses}")
    print(f"literal count: {literal_count}")


if __name__ == "__main__":
    main()
