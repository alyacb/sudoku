## Sudoku board ##
## by A.C.B. ##

from probability import *
from config import *
from typing import List, Union

class Element:
    def __init__(self, fixed: int = 0):
        self.likelies = {}
        if fixed == 0:
            for i in range(1, D + 1):
                self.likelies[i] = UNIFORM
        else:
            self.fix(fixed)
    
    def __str__(self):
        if self.fixed():
            return str(self.get())

        probs = {}
        # group by probability
        for i in self.likelies.items():
            p = str(i[1])
            v = str(i[0])
            if p not in probs:
                probs[p] = set([v])
            else:
                probs[p].add(v)

        str_arr = []
        for p in probs:
            s = probs[p]
            str_arr.append("{" + ",".join(sorted(s)) + "}:" + p)
        return " + ".join(str_arr)

    def p_space(self) -> int:
        return len(self.likelies)

    def impossible(self) -> bool:
        return len(self.likelies) == 0

    def fixed(self) -> bool:
        return len(self.likelies) == 1
    
    def get(self, i: int = 0) -> Union[int, Probability]:
        if i == 0:
            assert self.fixed()
            return next(iter(self.likelies))
        else:
            assert i >= 1 and i <= D
            if i in self.likelies:
                return self.likelies[i]
            else:
                return NEVER

    def fix(self, i: int):
        assert i in self.likelies

        for j in self.likelies:
            if j == i:
                self.likelies[j] = ALWAYS

        self.likelies = {}
        self.likelies[i] = ALWAYS
    
    def bump(self, i) -> bool:
        if i not in self.likelies:
            return False

        p = self.likelies.pop(i).value
        p_diff = p / len(self.likelies)

        for j in self.likelies:
            self.likelies[j] += p_diff
        return True

class Board:
    def __init__(self, other: 'Board' = None):
        self.grid = []
        if other is None:
            for _ in range(0, D):
                self.grid.append([])
                for d in range(0, D):
                    self.grid[-1].append(Element())
        else: # deepcopy!
            for r in range(0, D):
                self.grid.append([])
                for c in range(0, D):
                    e = other.grid[r][c]
                    e2 = Element()
                    e2.likelies = {}
                    for l in e.likelies:
                        e2.likelies[l] = Probability(e.likelies[l].value)

                    self.grid[-1].append(e2)
    
    def __str__(self):
        s_arr = []
        max_len = 0
        for row in self.grid:
            s_arr.append([])
            for column in row:
                s_e = str(column)
                if len(s_e) > max_len:
                    max_len = len(s_e)
                s_arr[-1].append(s_e)
        
        s = ""
        for r in range(0, len(s_arr)):
            if r % 3 == 0:
                s += "━" * len(s_arr[r])*(max_len + 1) + "━━\n"
            for c in range(0, len(s_arr)):
                if c % 3 == 0:
                    s += "┃"
                s_nxt = s_arr[r][c]
                s += s_nxt + " " * (max_len - len(s_nxt) + 1)
            s += "\n"
        
        return s
    
    def done(self):
        for row in self.grid:
            for e in row:
                if not e.fixed():
                    return False
        return True

    def validate(self):
        # first pass: is anything "impossible"?
        for row in self.grid:
            for e in row:
                if e.impossible():
                    return False
        
        # second pass: is anything "conflicting"?
        for i, constraint in enumerate(self.constraints()):
            cons_s = "Row"
            if i == 1:
                cons_s = "Col"
            elif i == 2:
                cons_s = "Block"

            for j, path in enumerate(constraint):
                seen = set([])
                for k, e in enumerate(path):
                    if e.fixed():
                        digit = e.get()
                        if digit in seen:
                            print("Conflict at {}#{}, position {}, digit {}".format(cons_s, j, k, digit))
                            return False
                        else:
                            seen.add(digit)
        return True

    # NOTE: uses 3 Constraints:
    # - rows
    # - columns
    # - 3x3 blocks
    def constraints(self) -> List[List[List[Element]]]:
        res = [[], [], []]
        bo = -3
        for r in range(0, len(self.grid)):
            res[0].append([])

            if r % 3 == 0:
                bo += 3

            for c in range(0, len(self.grid[r])):
                # row
                e = self.grid[r][c]
                res[0][-1].append(e)

                # column
                if len(res[1]) <= c:
                    res[1].append([])
                res[1][c].append(e)

                # block
                if r % 3 == 0 and c % 3 == 0:
                    res[2].append([])

                res[2][(c // 3) + bo].append(e)

        return res

    # get highest non-zero probability elements
    def shiniest_element(self) -> tuple:
        ret = None
        last_e = None
        for r in range(0, len(self.grid)):
            for c in range(0, len(self.grid[r])):
                e = self.grid[r][c]
                if e.fixed():
                    continue
                elif ret is None or e.p_space() < last_e.p_space():
                    ret = (r, c)
                    last_e = e

        return ret

    # "brush" probabilities to eliminate conflicting element probabilities
    def brush(self) -> int:
        changed = 0

        for constraint in self.constraints():
            for c in constraint: # each row, column, or block
                fixeds = set([])
                # get all "fixed" digits in elements
                for e in c:
                    if e.fixed():
                        fixeds.add(e.get())

                if len(fixeds) == len(c):
                    # we are done with this constraint!
                    continue

                # bump these fixed d values from other elements in constraint
                while len(fixeds) > 0:
                    d = fixeds.pop()
                    for e in c:
                        if e.fixed():
                            continue
                        if e.bump(d):
                            changed += 1

        return changed