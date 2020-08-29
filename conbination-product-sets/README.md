This is a work in progress, written to aid in my understanding of Erv Wilson's Combination Product Sets. Python 3 is required.

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

# summarize the hexanies contained in this eikosany
find_embedded_cps(eikosany, 4)
```

Dave Seidel, August 2020
