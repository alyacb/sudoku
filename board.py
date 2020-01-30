## Sudoku board ##
## by A.C.B. ##

from probability import *
from config import *
from typing import List, Union

class Element:
    def __init__(self, fixed: int = 0):
        self.impossibles = set([])
        self.likelies = {}
        if fixed == 0:
            for i in range(1, D + 1):
                self.likelies[i] = UNIFORM
        else:
            self.fix(fixed)
    
    def __str__(self):
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
        assert i not in self.impossibles

        for j in self.likelies:
            if j == i:
                self.likelies[j] = ALWAYS
                continue
            self.impossibles.add(j)

        self.likelies = {}
        self.likelies[i] = ALWAYS
    
    def bump(self, i) -> bool:
        if i in self.impossibles:
            return False

        p = self.likelies.pop(i).value
        p_diff = p / len(self.likelies)
        self.impossibles.add(i)

        for j in self.likelies:
            self.likelies[j] += p_diff
        return True

class Board:
    def __init__(self):
        self.grid = []
        for _ in range(0, D):
            self.grid.append([])
            for d in range(0, D):
                self.grid[-1].append(Element())
    
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
                s += "━" * len(s_arr[r])*(max_len + 1) + "\n"
            for c in range(0, len(s_arr)):
                if c % 3 == 0:
                    s += "┃"
                s_nxt = s_arr[r][c]
                s += s_nxt + " " * (max_len - len(s_nxt) + 1)
            s += "\n"
        
        return s

    # NOTE: uses 3 Constraints:
    # - rows
    # - columns
    # - 3x3 blocks
    def constraints(self) -> List[List[List[Element]]]:
        res = [[], [], []]
        bc = 0
        blocks = 0
        for r in range(0, len(self.grid)):
            res[0].append([])
            for c in range(0, len(self.grid[r])):
                # row
                e = self.grid[r][c]
                res[0][-1].append(e)

                # column
                if len(res[1]) <= c:
                    res[1].append([])
                res[1][c].append(e)

                # block
                if blocks <= len(res[2]):
                    res[2].append([])
                res[2][-1].append(e)

                if bc % D == 0:
                    bc = 0
                    blocks += 1
                else:
                    bc += 1

        return res

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
                        if (e.bump(d)):
                            changed += 1

        return changed