"""
Ad-hoc functions purely for my own use
"""

from __future__ import annotations

from fractions import Fraction
from functools import reduce
from itertools import combinations, repeat
import math
from operator import mul
from pprint import pformat
from typing import Dict, List, Set, Tuple


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
