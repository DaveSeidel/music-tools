from fractions import Fraction
from functools import reduce
from itertools import combinations
from operator import mul
from typing import List


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
    def __init__(self, factors: List):
        self._size = len(factors)
        self._factors = factors
        self._orig_product = self._product = reduce(mul, factors, 1)
        self._frac = self.reduce()

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
        return self._product < other._product

    def __str__(self):
        return f"{self._factors} => {self.ratio()}"

    def ratio(self):
        return f"{self._frac if self._frac > 1 else '1/1'}"


class CPS(object):
    def __init__(self,
                 factors: List, choose: int = None,
                 name: str = "unnamed"):
        if not factors:
            raise ValueError("Empty list of factors")

        self._factors = factors
        self._factors_str = []
        for f in factors:
            self._factors_str.append(str(f))

        self._name = name
        self._transposition = 1
        self._transposition_str = "1"

        if not choose:
            choose = int(len(factors)/2)
        self._cps = [CpsElement(t) for t in combinations(factors, choose)]

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
            print(f"{self._name} 1/1 => {self._transposition_str}")
        for t in self._cps:
            print(t)

    def print_scale(self):
        scale = [t.ratio() for t in self._cps]
        print(f"{self._name} {'-'.join(self._factors_str)} @ {self._transposition_str}: {' '.join(scale)}")


def find_embedded_cps(cps: CPS, size: int):
    factors = set(cps.factors)
    embeds = combinations(cps.factors, size)
    for embed in embeds:
        embed = set(embed)
        mults = factors.difference(embed)
        for mult in mults:
            print(f"{sorted(embed)} * {mult}")


if __name__ == "__main__":

    # create an eikosany
    eiko_factors = (1, 3, 5, 7, 11, 13)
    eikosany = CPS(eiko_factors, name="eikosany")
    eikosany.explain()
    eikosany.print_scale()
    print("\n-----")

    # iterate through all the linear variations
    combos = combinations(eiko_factors, 3)
    for combo in combos:
        eikosany.transpose(reduce(mul, combo, 1), f"{combo[0]}*{combo[1]}*{combo[2]}")
        eikosany.explain()
        print()
        eikosany.print_scale()
        print("\n-----")

    print("\nHexanies contained in this Eikosany:")
    find_embedded_cps(eikosany, 4)
