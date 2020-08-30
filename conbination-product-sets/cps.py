from fractions import Fraction
from functools import reduce
from itertools import combinations
from operator import mul
from typing import List, Tuple


class Ratio(Fraction):
    @classmethod
    def octave_reduce(cls, thing):
        if not isinstance(thing, Fraction):
            thing = Fraction(thing)

        half = Fraction(1, 2)
        while thing > 2:
            thing *= half
        return thing


class CpsElement(object):
    def __init__(self,
                 factors: List,
                 multiplier: int = None):
        self._size = len(factors)
        self._factors = factors
        self._multiplier = multiplier
        if self._multiplier:
            self._factors = self._factors + (self._multiplier,)
        self._orig_product = self._product = reduce(mul, self._factors, 1)
        self._frac = self.reduce()

    @property
    def factors(self):
        return self._factors

    @property
    def ratio(self):
        return f"{self._frac if self._frac > 1 else '1/1'}"

    def reduce(self):
        return Ratio.octave_reduce(self._product)

    def div(self, divisor):
        prod = self._orig_product
        while divisor > prod:
            prod *= 2
        self._product = prod / Fraction(divisor)
        self._frac = self.reduce()
        return self

    def __lt__(self, other):
        if not isinstance(other, CpsElement):
            raise ValueError("Must compare against same type")
        return self._frac < other._frac

    def __str__(self):
        return f"{self._factors}\t=>\t{self.ratio}"


class CPS(object):
    def __init__(self,
                 factors: List,
                 multiplier: int = None,
                 choose: int = None,
                 name: str = "unnamed"):
        if not factors:
            raise ValueError("Empty list of factors")

        self._factors = factors
        self._factors_str = []
        for f in factors:
            self._factors_str.append(str(f))
        self._multiplier = multiplier

        self._name = name
        self._transposition = 1
        self._transposition_str = "1"

        if not choose:
            choose = int(len(factors)/2)
        self._cps = sorted([CpsElement(t, multiplier=self._multiplier)
                            for t in combinations(factors, choose)])

    @property
    def factors(self):
        return self._factors

    def transpose(self, expr, expr_str):
        self._transposition = expr
        self._transposition_str = expr_str
        transposed = []
        for t in self._cps:
            transposed.append(t.div(expr))
        self._cps = sorted(transposed)

    def explain(self):
        if self._name:
            print(f"{self._name} 1/1 = {self._transposition_str}")
        for t in self._cps:
            print(t)

    def get_scale(self, tabular=False):
        if tabular:
            scale = [f"{t.ratio:<9}" for t in self._cps]
            scl = ' '.join(scale)
        else:
            scale = [t.ratio for t in self._cps]
            scl = f"{self._name}: {'-'.join(self._factors_str)} @ {self._transposition_str}: {' '.join(scale)}"
        return scl

    def get_factors(self, stars=False):
        if stars:
            s = ','.join(['*'.join([str(f) for f in t.factors]) for t in self._cps])
        else:
            s = ','.join([str(t.factors) for t in self._cps])
        return s


def find_embedded_cps(cps: CPS,
                      size: int,
                      choose: int,
                      transpose: Tuple[int, str] = None):
    factors = set(cps.factors)
    embeds = list(combinations(cps.factors, size))
    for embed in embeds:
        embed = set(embed)
        mults = factors.difference(embed)
        for mult in mults:
            embed = sorted(embed)
            name = f"{embed} * {mult}"
            cps = CPS(embed, multiplier=mult, choose=choose, name=name)
            if transpose:
                cps.transpose(transpose[0], transpose[1])
            # cps.explain()
            print(f"{name}:\t{cps.get_scale(tabular=True)}")
            # print()


if __name__ == "__main__":

    # create an eikosany
    eiko_factors = (1, 3, 5, 7, 11, 13)
    eikosany = CPS(eiko_factors, name="eikosany")
    eikosany.explain()
    print(eikosany.get_scale())
    print(eikosany.get_factors(stars=True))
    print("\n-----")

    # iterate through all the linear variations
    combos = combinations(eiko_factors, 3)
    for combo in combos:
        eikosany.transpose(reduce(mul, combo, 1), f"{combo[0]}*{combo[1]}*{combo[2]}")
        eikosany.explain()
        print()
        print(eikosany.get_scale())
        print("\n-----\n")

    print("\n=====\n\nHexanies contained in this Eikosany:")
    eikosany.transpose(1*5*13, "1*5*13")
    eikosany.explain()
    print()
    print(eikosany.get_scale())
    print()
    find_embedded_cps(eikosany, 4, 2, transpose=(1*5*13, "1*5*13"))
