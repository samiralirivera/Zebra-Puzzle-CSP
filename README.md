<<<<<<< HEAD
# Zebra Puzzle CSP Implementation

This project implements the classic Zebra Puzzle (also known as Einstein's Puzzle) as a Constraint Satisfaction Problem (CSP) using Python.

## Problem Description

The puzzle involves five houses, each with different characteristics:
- Different colors
- Different nationalities
- Different candy preferences
- Different drinks
- Different pets

The goal is to determine:
1. In which house the zebra lives
2. In which house they drink water

## Implementation Details

The implementation uses the `python-constraint` library to solve the CSP. The problem is represented with:
- Variables: Nationalities, colors, candies, drinks, and pets
- Domains: House numbers (1-5)
- Constraints: All different constraints and specific puzzle constraints

## Running the Code

1. Install the required package:
```bash
pip install -r requirements.txt
```

2. Run the solver:
```bash
python zebra_puzzle.py
```

## Output

The program will output:
- The house number where the zebra lives
- The house number where water is drunk
- A complete breakdown of all house assignments
=======
# Zebra-Puzzle-CSP
>>>>>>> 5ccc2edd48270f4c85c16e289b579e67d4dbc103
