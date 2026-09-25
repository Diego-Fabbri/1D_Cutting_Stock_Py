# 1D Cutting Stock Problem (CSP)

A **Mixed Integer Linear Programming (MILP)** model in **Python** for the **1D Cutting Stock Problem**, built with the **[Pyomo](http://www.pyomo.org/)** optimization framework and solved via the **IBM ILOG CPLEX** solver.

## Overview

The 1D Cutting Stock Problem (CSP) is a classic combinatorial optimization problem in Operations Research. A set of items of different lengths must be cut from standard raw stock pieces of fixed length. The goal is to **satisfy the demand for each item type while using the minimum number of raw stocks**.

The model adopts a **pattern-based formulation**: all feasible cutting configurations (patterns) are enumerated in advance. Each pattern specifies how many pieces of each item type can be cut from a single raw stock. The decision variables represent how many times each pattern is applied. This formulation is widely used in manufacturing (paper, steel, glass, wood) wherever long raw materials must be cut into shorter pieces with minimum waste.

## Repository Contents

| File | Description |
|---|---|
| `1D_Cutting_Stock_Problem.py` | Python script implementing and solving the CSP via Pyomo and CPLEX |
| `1D_Cutting_Stock_Problem_Results.txt` | Solver output: execution time, active patterns, optimal stock count, and material balance |
| `1D Cutting Stock.pdf` | Mathematical formulation of the problem |

## Mathematical Formulation

### Sets

- $I$ = set of item types (index $i$)
- $J$ = set of feasible cutting patterns (index $j$)

### Parameters

- $L$ = length of the standard raw stock
- $l_i$ = length of item type $i$; $\forall\, i \in I$
- $d_i$ = demand (number of pieces required) of item type $i$; $\forall\, i \in I$
- $a_{ij}$ = number of pieces of item type $i$ cut in pattern $j$; $\forall\, i \in I,\ j \in J$
- $w_j$ = waste of pattern $j$: $w_j = L - \displaystyle\sum_{i \in I} l_i \cdot a_{ij}$; $\forall\, j \in J$

### Variable

- $x_j$ = number of raw stocks cut according to pattern $j$; $x_j \in \mathbb{Z}^+$, $\forall\, j \in J$

### Objective Function

**(1)** — Minimize total number of raw stocks used

$$
\displaystyle \min \sum_{j \in J} x_j
$$

### Constraints

**(2)** — Demand satisfaction: total pieces of item $i$ cut across all patterns must meet or exceed demand

$$
\displaystyle \sum_{j \in J} a_{ij} \cdot x_j \ge d_i \qquad \forall\, i \in I
$$

**(3)** — Non-negative integer variables

$$
x_j \in \mathbb{Z}^+ \qquad \forall\, j \in J
$$

> **Note on the pattern-based approach:** Constraint (2) uses $\ge$ rather than $=$ because overproduction is acceptable — cutting slightly more than demanded is a natural consequence of indivisible patterns. The waste $w_j$ is computed before optimization for each pattern $j$ and printed alongside the solution for traceability.

A copy of this formulation is also available as a standalone PDF in this repository.

## Example Instance

The script uses a hardcoded instance with **5 item types**, **20 cutting patterns**, and a raw stock of length **$L = 850$**:

**Item specifications:**

| Item $i$ | Length $l_i$ | Demand $d_i$ |
|:---:|---:|---:|
| 1 | 330 | 50 |
| 2 | 315 | 30 |
| 3 | 295 | 40 |
| 4 | 250 | 42 |
| 5 | 205 | 20 |

- **Total length demanded**: $330 \times 50 + 315 \times 30 + 295 \times 40 + 250 \times 42 + 205 \times 20 = 52{,}350$
- **Continuous lower bound**: $\lceil 52{,}350 / 850 \rceil = 62$ stocks

**Cutting pattern matrix $A$** (rows = items, columns = patterns):

$$
A = \begin{pmatrix}
1 & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 2 & 0 \\
1 & 0 & 2 & 0 & 0 & 0 & 1 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 & 0 \\
0 & 2 & 0 & 1 & 0 & 0 & 1 & 0 & 1 & 2 & 0 & 0 & 1 & 0 & 0 & 0 & 1 & 0 & 0 & 0 \\
0 & 1 & 0 & 0 & 2 & 0 & 0 & 2 & 2 & 0 & 1 & 1 & 1 & 3 & 0 & 0 & 0 & 2 & 0 & 1 \\
1 & 0 & 1 & 1 & 0 & 4 & 1 & 0 & 0 & 1 & 1 & 1 & 1 & 0 & 2 & 2 & 2 & 1 & 0 & 2
\end{pmatrix}
$$

The **optimal total stocks used is 66**, found in **0.08 seconds** — matching the Java version exactly. The 5 active patterns are:

| Pattern $j$ | Times used $x_j$ | Waste $w_j$ |
|:---:|---:|---:|
| 1 | 10 | 0 |
| 2 | 20 | 10 |
| 3 | 10 | 15 |
| 5 | 11 | 20 |
| 19 | 15 | 190 |
| **Total** | **66** | |

Full material balance:

| Metric | Value |
|---|---:|
| Continuous lower bound | 62 stocks |
| **Optimal stocks used** | **66 stocks** |
| Total stock length | 56,100 |
| Total length cut for items | 52,680 |
| **Total waste** | **3,420** |
| Item 1: cut vs demand | 51 vs 50 (+1 overproduction) |
| Items 2–5: cut vs demand | exact |

## Requirements

Install the required Python packages via pip:

```bash
pip install pyomo numpy pandas
```

**IBM ILOG CPLEX** must also be installed separately on your system. An academic license is available free of charge through the [IBM Academic Initiative](https://www.ibm.com/academic).

## Usage

1. Clone the repository:
   ```bash
   git clone https://github.com/Diego-Fabbri/1D_Cutting_Stock_Py.git
   cd 1D_Cutting_Stock_Py
   ```

2. Run the script:
   ```bash
   python 1D_Cutting_Stock_Problem.py
   ```

## Output

When executed, the script:
- Computes and prints the waste $w_j$ for each of the 20 cutting patterns before solving
- Builds the MILP model using Pyomo's `ConcreteModel` and prints the full model structure to the console
- Solves it via CPLEX and measures execution time
- Writes the results to `1D_Cutting_Stock_Problem_Results.txt`, including:
  - Execution time in seconds
  - Active patterns $x_j \ge 1$ and their usage counts
  - Optimal total number of stocks used (objective value)
  - Total length demanded, continuous lower bound, total stock length, total cut length, and total waste
  - Actual vs demanded pieces cut for each item type
