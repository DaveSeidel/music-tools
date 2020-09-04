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
            scl = ' '.join(scale)
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
            i:[] for i in range(6)
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


if __name__ == "__main__":

    #
    # Demo code showing some of the things you can do with the CPS class.
    # These sample functions are executed at the end of this file.
    #

    def transpose_and_spawn(parent: CPS,
                            tr: Tuple[int, Str],
                            length: int,
                            choose: int):
        if tr:
            parent.transpose(tr[0], tr[1])
        return parent.find_embedded_cps(length, choose, transpose=tr)

    def print_cps(cps: CPS) -> None:
        """
        Print stuff about a CPS instance
        """
        print(cps)
        print(f"\n{'ratios:':>10} {cps.list_scale()}")
        # print(f"\nterms:\t{cps.list_factors(stars=True)}")
        print(f"{'o_C notes:':>10} {cps.o_C_notes}")
        # print(cps._o_C_map)

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

    def print_hexanies(eikosany: CPS, transposition: Tuple[int, Str]) -> None:
        """
        Set 1/1 to ??? and print out all the embedded hexanies in various ways
        """
        print(f"\n=====\n\nHexanies contained in {eikosany.name}, 1/1 = {transposition[1]}:")
        eikosany.transpose(transposition[0], transposition[1])
        hexanies = eikosany.find_embedded_cps(4, 2, transpose=transposition)

        # human-readable ASCII table
        print(f"reference:\t\t{eikosany.list_scale(tabular=True)}")
        for hex in hexanies:
            print(f"{hex.name}:\t{hex.list_scale(tabular=True)}\t[{hex.product}]")

        print()

        # ratios
        print(f"1/1 = {transposition[1]}:")
        for hex in hexanies:
            print(f"{hex.name}:\t{hex.list_scale()}")

        print()

        # indexes relative to full eikosany
        for hex in hexanies:
            print(f"{hex.name}:\t{hex.relative_index}")


    def print_hexanies_csv(eikosany: CPS, transposition: Tuple[int, Str]) -> None:
        eikosany.transpose(transposition[0], transposition[1])
        hexanies = eikosany.find_embedded_cps(4, 2, transpose=transposition)

        print(f"{eikosany.name} @ {eikosany.transposition},{eikosany.list_factors(stars=True)}")
        print(f",{eikosany.list_scale(tabular=True, csv=True)}")

        for hex in hexanies:
            name = hex.name.replace(" ", "")
            name = name.replace(",", "-")
            print(f"{name},{hex.list_scale(tabular=True, csv=True)}")


    def print_hexanies_common_tones(eikosany: CPS, hexanies: List[CPS], index: int):
        ct = CPS.find_common_tones(hexanies, 0)
        print(f"Intersections for {hexanies[0].list_scale()} {hexanies[0].relative_index}\n")
        for k, v in ct.items():
            if len(v):
                # print(f"\tcommon tones: {k} -> {pformat([i.list_scale() for i in v])}\n")
                # print(f"common tones: {k} ->\n{pformat([i.relative_index for i in v])}\n")
                print(f"common tones: {k} ->\n{pformat([i.name for i in v])}\n")


    def print_hexanies2(eikosany: CPS) -> None:
        factors = {
            eval(f): f
            for f in eikosany.list_factors(stars=True).split(',')
        }
        sorted(factors.items(), key=lambda f: f[0])
        for n, s in factors.items():
            print(f"\n=====\n\n1/1 Hexanies contained in {eikosany.name}, 1/1 = {s}:")
            eikosany.transpose(n, s)
            print(f"{'Reference:':<19}\t{eikosany.list_scale(tabular=True)}")

            hexanies = eikosany.find_embedded_cps(4, 2, transpose=(n, s))
            for hex in hexanies:
                for i, r in enumerate(hex.ratios):
                    if r == 1:
                        print(f"{hex.name}:\t{hex.list_scale(tabular=True)}")
                if hex.product == 1*3*5*7:
                        print(f"{hex.name}:\t{hex.list_scale(tabular=True)}")

        print()

        print("All 1-3-5-7 hexanies across the set of eikosany transpositions")
        for n, s in factors.items():
            eikosany.transpose(n, s)
            hexanies = eikosany.find_embedded_cps(4, 2, transpose=(n, s))
            for hex in hexanies:
                if hex.product == 1*3*5*7:
                        print(f"{s:<7} {hex.name}:\t{hex.list_scale(tabular=True)}")
        print()

        # print("All 1-3-5-7 hexanies that start at 1/1 in their respective eikosany transpositions")
        # for n, s in factors.items():
        #     eikosany.transpose(n, s)
        #     hexanies = eikosany.find_embedded_cps(4, 2, transpose=(n, s))
        #     for hex in hexanies:
        #         if hex.product == 1*3*5*7 and hex.ratios[0] == 1:
        #                 print(f"{s:<7} {hex.name}:\t{hex.list_scale(tabular=True)}")

        # print()

    def collect_hexanies(parent: CPS, hexanies: List[CPS], names: List[str]) -> List[CPS]:
        hexanies = {hex.name.replace(' ', ''): hex for hex in hexanies}
        collection = [hexanies[name] for name in names]
 
        print("as ratios")
        for c in collection:
            print(f"{c.name:<19}\t{c.list_scale()}")
 
        print()
        for c in collection:
            print(f"{c.name:<19}\t{c.list_scale(tabular=True)}")
 
        print()
        print("as offsets")
        for c in collection:
            index = [f"{i:>3}" for i in c.relative_index]
            print(f"{c.name:<19}\t[{','.join(index)} ]")
 
        print()
        print("as o_C note values")
        for c in collection:
            notes = [f"{n:>5}" for n in c.o_C_notes]
            print(f"{c.name:<19}\t{','.join([n for n in notes])}")
 
        return collection
    
    #
    # Execute the demo code.
    #

    # create an eikosany
    eiko_factors = (1, 3, 5, 7, 11, 13)
    eikosany = CPS(eiko_factors, name="1-3-5-7-11-13 Eikosany")

    # do stuff with it
    # print_cps(eikosany)
    # print_cps_transpositions(eikosany, eiko_factors)

    # print_hexanies(eikosany, (1*3*5, "1*3*5"))
    # print_hexanies_csv(eikosany, (1*3*5, "1*3*5"))

    # print_hexanies2(eikosany)

    # hexanies = transpose_and_spawn(eikosany, (1*3*5, "1*3*5"), 4, 2)
    # eikosany.transpose(1*3*5, "1*3*5")
    # print_cps(eikosany)
    # print()

    # for i in range(11):
    #     print_hexanies_common_tones(eikosany, hexanies, i)

    print("\nSequence with common tones, eikosany 1/1 = 1*5*13\n")
    eikosany.transpose(1*5*13, "1*5*13")
    print_cps(eikosany)
    print()
    hexanies = transpose_and_spawn(eikosany, (1*5*13, "1*5*13"), 4, 2)
    collected = collect_hexanies(eikosany,
                                 hexanies,
                                 ('[1,3,5,7]*11',  '[1,3,5,11]*7', '[1,3,7,11]*5', '[1,3,5,13]*11'))
    print()
    notes_used = []
    indexes_used = []
    for c in collected:
        notes_used.extend(c.o_C_notes)
        indexes_used.extend(c.relative_index)

    notes_used = {n for n in notes_used}
    all_notes = {n for n in eikosany.o_C_notes}
    unused_notes = all_notes - notes_used
    notes_used = sorted([n for n in notes_used])
    unused_notes = sorted([n for n in unused_notes])
    print(f"used: {notes_used} len={len(notes_used)}")
    # print(f"unused: {unused_notes} len={len(unused_notes)}")

    # indexes_used = {i for i in indexes_used}
    # indexes_used = sorted([i for i in indexes_used])
    # print(f"indexes: {indexes_used}")

    for c in collected:
        indexes = []
        for n in c.o_C_notes:
            indexes.append(notes_used.index(n))
        print(f"indexes for {c.name}: {indexes}")

    # print(eikosany)
    # print()
    # dekany = CPS((1, 3, 5, 7, 11), choose=3, name="1-3-5-7-11 dekany")
    # print(dekany)
    # print(dekany.list_scale(tabular=True))

    # print()
    # dekanies = transpose_and_spawn(eikosany, (1*3*13, "1*3*13"), 5, 3)
    # for dek in dekanies:
    #     print(dek)
    #     print(dek.list_scale())

    # print("as ratios")
    # for dek in dekanies:
    #     print(f"{dek.name:<19}\t{dek.list_scale()}")
    # print()
    # for dek in dekanies:
    #     print(f"{dek.name:<19}\t{dek.list_scale(tabular=True)}")
    # print()
    # print("as offsets")
    # for dek in dekanies:
    #     index = [f"{i:>3}" for i in dek.relative_index]
    #     print(f"{dek.name:<19}\t[{','.join(index)} ]")
