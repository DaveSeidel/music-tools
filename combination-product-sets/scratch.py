"""
Scratch pad
"""

from cps import CpsElement, CPS
from cps_functions import *


# create an eikosany
eiko_factors = (1, 3, 5, 7, 11, 13)
eikosany = CPS(eiko_factors, name="1-3-5-7-11-13 Eikosany")

# do stuff with it
print_cps(eikosany)
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

# print("\nSequence with common tones, eikosany 1/1 = 1*5*13\n")
# eikosany.transpose(1*5*13, "1*5*13")
# print_cps(eikosany)
# print()
# hexanies = transpose_and_spawn(eikosany, (1*5*13, "1*5*13"), 4, 2)
# collected = collect_hexanies(eikosany,
#                              hexanies,
#                              ('[1,3,5,7]*11',  '[1,3,5,11]*7', '[1,3,7,11]*5', '[1,3,5,13]*11'))
# print()
# notes_used = []
# indexes_used = []
# for c in collected:
#     notes_used.extend(c.o_C_notes)
#     indexes_used.extend(c.relative_index)

# notes_used = {n for n in notes_used}
# all_notes = {n for n in eikosany.o_C_notes}
# unused_notes = all_notes - notes_used
# notes_used = sorted([n for n in notes_used])
# unused_notes = sorted([n for n in unused_notes])
# print(f"used: {notes_used} len={len(notes_used)}")
# print(f"unused: {unused_notes} len={len(unused_notes)}")

# indexes_used = {i for i in indexes_used}
# indexes_used = sorted([i for i in indexes_used])
# print(f"indexes: {indexes_used}")

# for c in collected:
#     indexes = []
#     for n in c.o_C_notes:
#         indexes.append(notes_used.index(n))
#     print(f"indexes for {c.name}: {indexes}")

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

# hexanies = transpose_and_spawn(eikosany, (1*3*5, "1*3*5"), 4, 2)

# print("\n===== by ratios =====\n")
# srtd = sorted(hexanies, key=lambda cps: cps.ratios)
# for s in srtd:
#     print(f"{s.name:<19}\t{s.list_scale(tabular=True)}")

# print()
# for s in srtd:
#     print(f"{s.name_csv},{s.list_scale(tabular=True, csv=True)}")

# for i, s in enumerate(srtd):
#     # print(f"; {s.name}")
#     # print(f"{s.list_scale(csv=True)}")
#     print(f"; {s.name}\n"
#           f"gi_tab_{i} = ftgen(0, 0, 128, -51,\n"
#           f"                   6, 2, 297.989, 60,\n"
#           f"                   {s.list_scale(csv=True)})\n")

# print("\n===== by ratios, reversed =====\n")
# srtd = sorted(hexanies, key=lambda cps: cps.ratios[::-1], reverse=True)
# for s in srtd:
#     print(f"{s.name:<19}\t{s.list_scale(tabular=True)}")

# print("\n===== by factors =====\n")
# srtd = sorted(hexanies, key=lambda cps: cps.factors)
# for s in srtd:
#     print(f"{s.name:<19}\t{s.list_scale(tabular=True)}")

# print("\n===== by product =====\n")
# srtd = sorted(hexanies, key=lambda cps: cps.product)
# for s in srtd:
#     print(f"{s.name:<19}\t{s.list_scale(tabular=True)}")
