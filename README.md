# SAT Solver Report
By: Maxwell Smiley  & Leo Bonequi

## Introduction
This report describes the design and implementation of a Boolean SAT solver in Python. The program accepts Boolean expressions in Conjunctive Normal Form (CNF), representing a Boolean expression as a conjunction of one or more clauses. The solver determines satisfiability, enumerates all satisfying assignments, supports fixed variable assignments, compares two functions via XOR equivalence checking, and computes Minimum Satisfying Assignments (MSAs)

___
## Methods and Algorithms:
### Input Parsing
The parser accepts CNF expressions using '+' for OR, '.' for AND, and '~' for NOT. Clauses are delimited by '.' or parentheses and parsed via regular expressions. Each clause is stored as a list of literal objects, which evaluate to True, False, or None (unassigned) at runtime.
Solver
### Backtracking SAT Solver

The core solver uses recursive backtracking and unit propagation as discussed in class. For each unassigned variable, both True and False are tried in sequence. The algorithm terminates a branch early if the partial assignment already makes any clause false, and uses unit propagation to prune the search space further. A solution is only recorded once all variables are fully assigned, ensuring all distinct satisfying combinations are found. We also implemented a faster method which terminates partially assigned branches where every clause evaluates to True, at the cost of allowing don't cares in solutions.

___ 
## Roles and Responsibilities:

### Leo Bonequi:

•        Core backtracking SAT solver and solution enumeration.

•        Don't Care compression and post-processing algorithms.

•        Underlying data structures

### Maxwell Smiley:

•        Unit propagation with correct backtracking and state restoration.

•        MSA computation method.

•        User input parsing and menu interface for running program. 

  ___
# Operations:

## Unit Propagation

Unit propagation is applied at each node of the search tree before branching. If any clause contains exactly one unassigned literal and no satisfied literal, that literal is forced to satisfy the clause. All assignments made by unit propagation are tracked and undone on backtrack to maintain correct solver state. This heuristic significantly reduces the search space by forcing implied assignments early.

## Fixed Variable Assignments

The solver supports pre-assigning any subset of variables before search begins. The user provides assignments in the format 'x1=1 x2=0', which are applied to the literal values array prior to backtracking. The solver then finds all satisfying combinations consistent with those fixed values.

## Minimum Satisfying Assignment

The MSA algorithm works by getting all the satisfyability solutions via the sat solver method, then repeatedly merging solution pairs with single literal differences until none can be combined. Solutions are already partially simplified via the recursive backtracking method utilizing don’t cares, so some time is saved over exhaustive search. 

## Validation:

The solver results were validated using the pyEDA Boolean algebra library when applicable. For the same CNF inputs, pyEDA was used to confirm satisfiability results and verify that the returned solutions matched the expected output
