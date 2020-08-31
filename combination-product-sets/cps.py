from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import combinations, repeat
from operator import mul
from typing import Dict, List, Tuple


class Ratio(Fraction):
    """
    Extend Fraction class with method to octave reduce a ratio.
    """
    @classmethod
    def octave_reduce(cls, thing: Ratio) -> Ratio:
        half = Ratio(1, 2)
        while thing > 2:
            thing *= half
        return thing


class CpsElement(object):
    """
    Describes one element of a CPS, encapsulating the factors and including
    suppport for an optional multiplier for use with a CPS embedded within
    a larger CPS (e.g., hexanies within an eikosany).
    """
    def __init__(self,
                 factors: List[int],
                 multiplier: int = None):
        if not factors:
            raise ValueError("No factors specified")

        self._size = len(factors)
        self._factors = tuple(sorted(factors))

        self._multiplier = multiplier
        if self._multiplier:
            self._factors = tuple(sorted(self._factors + (self._multiplier,)))

        self._orig_product = self._product = reduce(mul, self._factors, 1)
        self._frac = self.reduce()

    @property
    def factors(self) -> List[int]:
        return self._factors

    @property
    def product(self) -> Ratio:
        return self._product

    @property
    def ratio(self) -> str:
        return f"{self._frac if self._frac > 1 else '1/1'}"

    def reduce(self) -> Ratio:
        return Ratio.octave_reduce(self._product)

    def div(self, divisor: int) -> CpsElement:
        prod = self._orig_product
        while divisor > prod:
            prod *= 2
        self._product = prod / Ratio(divisor)
        self._frac = self.reduce()
        return self

    def __lt__(self, other: CpsElement) -> bool:
        if not isinstance(other, CpsElement):
            raise ValueError("Must compare against same type")
        return self._frac < other._frac

    def __str__(self) -> str:
        return f"{self._factors}\t=>\t{self.ratio}"


class CPS(object):
    """
    Describes an arbitrary CPS, given a list of factors and a size. Optional multipler
    for a CPS which is embedded within a larger CPS (e.g., a hexany within an eikosany).
    """
    def __init__(self,
                 factors: List[int],
                 choose: int = None,
                 multiplier: int = None,
                 name: str = None,
                 parent: CPS = None):
        if not factors:
            raise ValueError("No factors specified")

        self._factors = factors
        self._factors_str = [str(f) for f in factors]
        self._multiplier = multiplier

        self._name = name if name else f"unamed {'-'.join(self._factors_str)}"
        self._transposition = 1
        self._transposition_str = "1"

        self._map = None
        self._parent = parent
        self._relative_map = None
        self._relative_index = None

        if not choose:
            choose = int(len(factors)/2)
        self._cps = sorted([CpsElement(combo, multiplier=self._multiplier)
                            for combo in combinations(factors, choose)])
        self._size = len(self._cps)
        self._build_maps()

    @property
    def name(self) -> str:
        return self._name

    @property
    def size(self) -> int:
        return self._size

    @property
    def factors(self) -> List[int]:
        return self._factors

    @property
    def transposition(self) -> str:
        return self._transposition_str

    @property
    def parent(self) -> Union[CPS, None]:
        return self._parent

    @property
    def map(self) -> Dict[str, int]:
        return self._map

    @property
    def relative_map(self) -> Dict[str, int]:
        return self._relative_map

    @property
    def relative_index(self) -> Union[List[int], None]:
        return self._relative_index

    def __str__(self) -> str:
        lines = []
        if self._name:
            lines.append(f"{self._name}, 1/1 = {self._transposition_str}")
        for elm in self._cps:
            lines.append(str(elm))
        return '\n'.join(lines)

    def transpose(self, expr: int, expr_str: str) -> None:
        self._transposition = expr
        self._transposition_str = expr_str

        transposed = []
        for elm in self._cps:
            transposed.append(elm.div(expr))
        self._cps = sorted(transposed)

        self._build_maps()

    def list_scale(self,
                   tabular: bool = False,
                   indexed: bool = False,
                   csv: bool = False) -> str:
        if tabular:
            if self._parent:
                sep = ',' if csv else ' '
                blank = "" if csv else "---      "
                ref = list(repeat(blank, self._parent.size))
                for pos, i in enumerate(self.relative_index):
                    ref[i] = f"{self._cps[pos].ratio}" if csv else f"{self._cps[pos].ratio:<9}"
                scl = sep.join(ref)
            else:
                sep = ',' if csv else ' '
                if csv:
                    scale = [f"{elm.ratio}" for elm in self._cps]
                else:
                    scale = [f"{elm.ratio:<9}" for elm in self._cps]
                scl = sep.join(scale)
        else:
            scale = [elm.ratio for elm in self._cps]
            # scl = f"{self._name}: {'-'.join(self._factors_str)} @ {self._transposition_str}: {' '.join(scale)}"
            scl = ' '.join(scale)
        return scl

    def list_factors(self, stars: bool = False) -> str:
        if stars:
            s = ','.join(['*'.join([str(f) for f in elm.factors]) for elm in self._cps])
        else:
            s = ','.join([str(elm.factors) for elm in self._cps])
        return s

    def _build_maps(self):
        if self._parent:
            # map factors relative to parent CPS
            self._relative_map = {
                str(elm.factors): self._parent.map[str(elm.factors)]
                for elm in self._cps
            }

            # list of reletive indexes
            self._relative_index = [self._relative_map[str(elm.factors)] for elm in self._cps]

        # map factors to index values
        self._map = {
            str(elm.factors): i
            for i, elm, in enumerate(self._cps)
        }

    def find_embedded_cps(self,
                          size: int,
                          choose: int,
                          transpose: Tuple[int, str] = None) -> List[CPS]:
        factors = set(self.factors)
        embeds = list(combinations(self.factors, size))
        cps_list = []

        for embed in embeds:
            embed = set(embed)
            mults = sorted(factors.difference(embed))
            for mult in mults:
                embed = sorted(embed)
                name = f"{embed}*{mult}"
                cps = CPS(embed, multiplier=mult, choose=choose, name=name, parent=self)
                if transpose:
                    cps.transpose(transpose[0], transpose[1])
                cps_list.append(cps)

        return cps_list


if __name__ == "__main__":

    #
    # Demo code showing some of the things you can do with the CPS class.
    # These sample functions are executed at the end of this file.
    #

    def print_cps(cps: CPS) -> None:
        """
        Print stuff about a CPS instance
        """
        print(cps)
        print(f"\nratios:\t{cps.list_scale()}")
        print(f"\nterms:\t{cps.list_factors(stars=True)}")

    def print_cps_transpositions(cps: CPS, factors: List[int]) -> None:
        """
        Print all the transpositions of a CPS instance
        """
        combos = combinations(factors, 3)
        for combo in combos:
            cps.transpose(reduce(mul, combo, 1), f"{combo[0]}*{combo[1]}*{combo[2]}")
            print("\n-----\n")
            print(cps)
            print()
            # print(cps.get_scale())

    def print_hexanies(eikosany: CPS) -> None:
        """
        Set 1/1 to 1*5*7 and print out all the embedded hexanies in various ways
        """
        print(f"\n=====\n\nHexanies contained in {eikosany.name}, 1/1 = 1*5*3:")
        eikosany.transpose(1*5*13, "1*5*13")
        hexanies = eikosany.find_embedded_cps(4, 2, transpose=(1*5*13, "1*5*13"))

        # human-readable ASCII table
        print(f"eikosany:\t\t{eikosany.list_scale(tabular=True)}")
        for hex in hexanies:
            print(f"{hex.name}:\t{hex.list_scale(tabular=True)}")
        print()

        # ratios
        for hex in hexanies:
            print(f"{hex.name}:\t{hex.list_scale()}")
        print()

        # indexes relative to full eikosany
        for hex in hexanies:
            print(f"{hex.name}:\t{hex.relative_index}")

        # CSV-formatted table
        print("\n\n=====\n\n")
        print(f"{eikosany.name} @ {eikosany.transposition},{eikosany.list_factors(stars=True)}")
        print(f",{eikosany.list_scale(tabular=True, csv=True)}")
        for hex in hexanies:
            name = hex.name.replace(" ", "")
            name = name.replace(",", "-")
            print(f"{name},{hex.list_scale(tabular=True, csv=True)}")

    #
    # Execute the demo code.
    #

    # create an eikosany
    eiko_factors = (1, 3, 5, 7, 11, 13)
    eikosany = CPS(eiko_factors, name="1-3-5-7-11-13 Eikosany")

    # do stuff with it
    print_cps(eikosany)
    print_cps_transpositions(eikosany, eiko_factors)
    print_hexanies(eikosany)
