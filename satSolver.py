class literal:
    def __init__(self, identity) -> None:
        self.identity: str = identity

    def eval(self, map):
        if "~" in self.identity:
            val = map[self.identity[1]]
            return 0 if val == 1 else 1
        else:
            return map[self.identity]

    def __str__(self) -> str:
        return self.identity

    def __repr__(self) -> str:
        return self.identity


def parseInput(input):
    terms: list[list[literal]] = list()
    term: list[literal] = list()
    negative = False

    for c in input:
        if c == "." or c == ")":
            if term:
                terms.append(term)
                term = list()
        elif c == "~":
            negative = True
        elif c.isdigit():
            if negative:
                term.append(literal("~" + c))
                negative = False
            else:
                term.append(literal(c))
    if term:
        terms.append(term)
    return terms


print(parseInput("(~x1+ x2) (x3 + ~x4) x1"))
