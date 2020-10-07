from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import combinations, repeat
import math
from operator import mul
from pprint import pformat
from typing import Dict, List, Set, Tuple


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

        self._multiplier = multiplier if multiplier else 0
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

    @property
    def ratio_n(self) -> Ratio:
        return self._frac

    @property
    def o_C_note(self) -> int:
        return round(1536 * (math.log(self._frac) / math.log(2)))

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

        self._product = reduce(mul, self._factors, 1)

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
    def name_csv(self) -> str:
        return self._name.replace(', ', '-')

    @property
    def size(self) -> int:
        return self._size

    @property
    def factors(self) -> List[int]:
        return self._factors

    @property
    def product(self) -> int:
        return self._product

    @property
    def transposition(self) -> str:
        return self._transposition_str

    @property
    def multiplier(self) -> int:
        return self._multiplier

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

    @property
    def products(self) -> Set[str]:
        return {str(elm.product) for elm in self._cps}

    @property
    def ratios(self) -> List[Ratio]:
        return [elm.ratio_n for elm in self._cps]

    @property
    def o_C_notes(self) -> List[int]:
        return [elm.o_C_note for elm in self._cps]

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
                   simple: bool = False,
                   csv: bool = False) -> str:
        if tabular:
            if self._parent:
                sep = ',' if csv else ' '
                blank = "" if csv else "        " if simple else ".        "
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
            sep = ', ' if csv else ' '
            scl = sep.join(scale)
        return scl

    def list_factors(self, stars: bool = False) -> str:
        if stars:
            s = ','.join(['*'.join([str(f) for f in elm.factors]) for elm in self._cps])
        else:
            s = ','.join([str(elm.factors) for elm in self._cps])
        return s

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

    @classmethod
    def find_common_tones(cls,
                          cps_list: List[CPS],
                          index: Union[int, None] = None) -> Dict[int, List[CPS]]:
        """
        Given a list of CPS instances compare the one indicated by the index parameter
        to the others in the list, based on how many tones are in common between the
        selected CPS and the others in the list.

        Returns a dict where the key is the number of common tones, and the value is
        a list of the CPS instances that meet that criterion.
        """
        product_sets = []
        for cps in cps_list:
            product_sets.append(cps.products)

        # analyze the first one
        ps = product_sets[0]
        intersections = {
            i: [] for i in range(6)
        }

        for i, other in enumerate(product_sets[1:]):
            inter = ps.intersection(other)
            mag = len(inter)
            intersections[mag].append(i+1)

        return {
            k: [cps_list[i] for i in v] for k, v in intersections.items()
        }

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

        self._o_C_map = {
            n: i for i, n in enumerate(self.o_C_notes)
        }
