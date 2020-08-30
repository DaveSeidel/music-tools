This is a work in progress, written to aid in my understanding of Erv Wilson's Combination Product Sets

Requires Python 3 (written and tested with Python 3.8.3).

The `CPS` class allows you to create any CPS, given a list of factors and the size of the combination.

The `find_embedded_cps()` function derives and prints out the instances of smaller types of CPS contained within a CPS instance.

Examples:
```
# create a hexany
hexany = CPS((1, 3, 5, 7), 2)

# decide where the 1/1 is
hexany.transpose(1*3, "1*3")

# print the resulting scale ratios
hexany.print_scale()
```

```
# create an eikosany
eikosany = CPS((1, 3, 5, 7, 11, 13), 3)

# print info about the eikosany
print(eikosany)

# summarize the hexanies contained in this eikosany, using 1*5*13 as 1/1
hexanies = eikosany.find_embedded_cps(4, 2, transpose=(1*5*13, "1*5*13"))
for hex in hexanies:
    print(f"{hex.name}:\t{hex.get_scale(tabular=True)}")
```

Execute the file (`python cps.py` or `python3 cps.py`) for a longer demonstration with more details.

Dave Seidel, August 2020
