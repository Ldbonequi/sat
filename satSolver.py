class literal:
    def __init__(self, identity) -> None:
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


def parseInput(input):
    """
    takes a cnf expression and returns a count of the literals and a list of terms
    params:
        input: cnf expression as string
    """
    terms: list[list[literal]] = list()
    term: list[literal] = list()
    negative: bool = False
    literals: set = set()

    for c in input:
        if c == "." or c == ")":  # and, start new term
            if term:
                terms.append(term)
                term = list()
        elif c == "~":  # next number is negative
            negative = True
        elif c.isdigit():  # found literal
            if negative:
                term.append(literal("~x" + c))
                negative = False
            else:
                term.append(literal("x" + c))
            literals.add(c)

    if term:
        terms.append(term)
    return len(literals), terms


def main():
    literal_count: int
    terms: list[list[literal]]
    literal_count, terms = parseInput("(~x1+ x2) (x3 + ~x4) x1")
    print(f"terms: {terms}")


if __name__ == "__main__":
    main()
