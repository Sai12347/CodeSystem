#!/usr/bin/env python3
"""Generate matrix problems 54-83 for AlgoPlay (batch 2)."""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "matrices"


def py_type(t: str) -> str:
    if t == "void":
        return "None"
    if t.endswith("[]"):
        return f"List[{py_type(t[:-2])}]"
    if t.startswith("List<") and t.endswith(">"):
        return f"List[{py_type(t[5:-1])}]"
    return {
        "int": "int",
        "long": "int",
        "Integer": "int",
        "Long": "int",
        "double": "float",
        "boolean": "bool",
        "char": "str",
        "String": "str",
    }[t]


def _grid_from_rows(rows: list[str]) -> list[list[str]]:
    return [list(r) for r in rows]


def _rng_int_grid(seed: int, m: int, n: int, lo: int, hi: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)]


def _rng_bin_grid(seed: int, m: int, n: int, p_one: float = 0.5) -> list[list[int]]:
    rng = random.Random(seed)
    return [[1 if rng.random() < p_one else 0 for _ in range(n)] for _ in range(m)]


def _rng_obstacle_grid(seed: int, m: int, n: int, p_wall: float = 0.18) -> list[list[int]]:
    rng = random.Random(seed)
    g = [[(-1 if rng.random() < p_wall else rng.randint(1, 50)) for _ in range(n)] for _ in range(m)]
    g[0][0] = rng.randint(1, 50)
    return g


def _rng_chessboard(seed: int, n: int, valid: bool = True) -> list[list[int]]:
    rng = random.Random(seed)
    start = rng.randint(0, 1)
    g = [[(r + c + start) % 2 for c in range(n)] for r in range(n)]
    rows = list(range(n))
    cols = list(range(n))
    rng.shuffle(rows)
    rng.shuffle(cols)
    res = [[g[r][c] for c in cols] for r in rows]
    if not valid:
        res[0][0] ^= 1
    return res


def _rng_mirror_grid(seed: int, m: int, n: int) -> list[list[str]]:
    rng = random.Random(seed)
    choices = [".", ".", ".", ".", "/", "\\"]
    return [[rng.choice(choices) for _ in range(n)] for _ in range(m)]


def _rng_rook_board(seed: int, m: int, n: int) -> list[list[str]]:
    rng = random.Random(seed)
    choices = [".", ".", ".", ".", ".", "p", "B"]
    g = [[rng.choice(choices) for _ in range(n)] for _ in range(m)]
    g[rng.randrange(m)][rng.randrange(n)] = "R"
    return g


def _rng_queens_case(seed: int, n: int, num_queens: int) -> dict:
    rng = random.Random(seed)
    kr, kc = rng.randrange(n), rng.randrange(n)
    used = {(kr, kc)}
    queens = []
    while len(queens) < num_queens:
        r, c = rng.randrange(n), rng.randrange(n)
        if (r, c) not in used:
            used.add((r, c))
            queens.append([r, c])
    return {"n": n, "queens": queens, "king": [kr, kc]}


def _rng_mines(seed: int, n: int, count: int) -> list[list[int]]:
    rng = random.Random(seed)
    used = set()
    res = []
    while len(res) < count:
        r, c = rng.randrange(n), rng.randrange(n)
        if (r, c) not in used:
            used.add((r, c))
            res.append([r, c])
    return res


def _rng_illumination(seed: int, n: int, num_lamps: int, num_queries: int) -> dict:
    rng = random.Random(seed)
    lamps = [[rng.randrange(n), rng.randrange(n)] for _ in range(num_lamps)]
    queries = []
    for i in range(num_queries):
        if i % 3 == 0 and lamps:
            lr, lc = rng.choice(lamps)
            qr = min(n - 1, max(0, lr + rng.randint(-1, 1)))
            qc = min(n - 1, max(0, lc + rng.randint(-1, 1)))
            queries.append([qr, qc])
        else:
            queries.append([rng.randrange(n), rng.randrange(n)])
    return {"n": n, "lamps": lamps, "queries": queries}


def _rng_num_matrix_2d_ops(seed: int, m: int, n: int, num_ops: int) -> dict:
    rng = random.Random(seed)
    mat = [[rng.randint(-50, 50) for _ in range(n)] for _ in range(m)]
    ops = ["NumMatrix2D"]
    args = [[mat]]
    for _ in range(num_ops):
        if rng.random() < 0.45:
            ops.append("update")
            args.append([rng.randrange(m), rng.randrange(n), rng.randint(-50, 50)])
        else:
            r1, r2 = sorted([rng.randrange(m), rng.randrange(m)])
            c1, c2 = sorted([rng.randrange(n), rng.randrange(n)])
            ops.append("sumRegion")
            args.append([r1, c1, r2, c2])
    return {"ops": ops, "args": args}


def _rng_subrect_ops(seed: int, m: int, n: int, num_ops: int) -> dict:
    rng = random.Random(seed)
    rect = [[rng.randint(1, 100) for _ in range(n)] for _ in range(m)]
    ops = ["SubrectangleQueries"]
    args = [[rect]]
    for _ in range(num_ops):
        if rng.random() < 0.45:
            r1, r2 = sorted([rng.randrange(m), rng.randrange(m)])
            c1, c2 = sorted([rng.randrange(n), rng.randrange(n)])
            ops.append("updateSubrectangle")
            args.append([r1, c1, r2, c2, rng.randint(1, 1000)])
        else:
            ops.append("getValue")
            args.append([rng.randrange(m), rng.randrange(n)])
    return {"ops": ops, "args": args}


def _rng_sum_queries(seed: int, n: int, q: int) -> dict:
    rng = random.Random(seed)
    queries = [[rng.randint(0, 1), rng.randrange(n), rng.randint(0, 1000)] for _ in range(q)]
    return {"n": n, "queries": queries}


TASKS: list[dict] = []

# ============================================================================
# Subtopic 1: Spiral Traversal (54 - 59)
# ============================================================================

TASKS.append({
    "slug": "54-sort-concentric-matrix-rings",
    "title": "Sort Concentric Matrix Rings",
    "difficulty": "Medium",
    "subtopic": "Spiral Traversal",
    "companies": ["Google", "Amazon", "Bloomberg"],
    "desc": (
        "You are given an `m x n` integer matrix `grid`. The matrix can be decomposed into concentric rectangular "
        "layers (rings) starting from the outermost border (`layer = 0`) and moving inward.\n\n"
        "Read each concentric layer in **clockwise** order starting from its top-left corner `(layer, layer)`: "
        "left-to-right along its top edge, top-to-bottom along its right edge, right-to-left along its bottom edge, "
        "and bottom-to-top along its left edge. (If the innermost layer degenerates to a single row, single column, "
        "or single cell, read those cells left-to-right or top-to-bottom without duplicates.)\n\n"
        "Sort the values within each layer independently in **non-decreasing** order, write them back along the same "
        "clockwise order of that layer, and return the resulting matrix."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 100",
        "-10^5 <= grid[i][j] <= 10^5",
    ],
    "hints": [
        "Process layers from top = 0, left = 0 inward while top <= bottom and left <= right, collecting the coordinates of the current layer in clockwise order.",
        "Sort the collected values for that layer and assign them back to the exact same sequence of coordinates.",
    ],
    "explanations": [
        "The outer ring of 8 elements [9,8,7,6,5,4,3,2] sorts clockwise into [2,3,4,5,6,7,8,9], while the single center cell 1 stays at (1, 1).",
        "In a 2x4 matrix there is a single ring of 8 cells; sorting clockwise places the smallest values along the top row left-to-right and the largest along the bottom row right-to-left.",
        "A single-row matrix has one degenerate ring of 4 cells sorted left-to-right.",
    ],
    "time": "O(m * n * log(m + n))",
    "space": "O(m * n)",
    "method": "sortMatrixRings",
    "params": [("grid", "int[][]")],
    "ret": "int[][]",
    "py": """        m, n = len(grid), len(grid[0])
        res = [[0] * n for _ in range(m)]
        top, bottom, left, right = 0, m - 1, 0, n - 1
        while top <= bottom and left <= right:
            coords = []
            for c in range(left, right + 1):
                coords.append((top, c))
            for r in range(top + 1, bottom + 1):
                coords.append((r, right))
            if bottom > top and right > left:
                for c in range(right - 1, left - 1, -1):
                    coords.append((bottom, c))
                for r in range(bottom - 1, top, -1):
                    coords.append((r, left))
            vals = sorted(grid[r][c] for r, c in coords)
            for (r, c), v in zip(coords, vals):
                res[r][c] = v
            top += 1
            bottom -= 1
            left += 1
            right -= 1
        return res""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        int top = 0, bottom = m - 1, left = 0, right = n - 1;
        while (top <= bottom && left <= right) {
            List<int[]> coords = new ArrayList<>();
            for (int c = left; c <= right; c++) coords.add(new int[]{top, c});
            for (int r = top + 1; r <= bottom; r++) coords.add(new int[]{r, right});
            if (bottom > top && right > left) {
                for (int c = right - 1; c >= left; c--) coords.add(new int[]{bottom, c});
                for (int r = bottom - 1; r > top; r--) coords.add(new int[]{r, left});
            }
            int sz = coords.size();
            int[] vals = new int[sz];
            for (int i = 0; i < sz; i++) {
                int[] p = coords.get(i);
                vals[i] = grid[p[0]][p[1]];
            }
            Arrays.sort(vals);
            for (int i = 0; i < sz; i++) {
                int[] p = coords.get(i);
                res[p[0]][p[1]] = vals[i];
            }
            top++;
            bottom--;
            left++;
            right--;
        }
        return res;""",
    "visible": [
        {"grid": [[9, 8, 7], [2, 1, 6], [3, 4, 5]]},
        {"grid": [[8, 3, 5, 1], [2, 7, 4, 6]]},
        {"grid": [[5, -2, 9, 0]]},
    ],
    "hidden": [
        {"grid": [[42]]},
        {"grid": [[4], [-1], [3], [2]]},
        {"grid": [[4, 3], [2, 1]]},
        {"grid": [[10, 20, 30, 40], [50, 4, 3, 60], [70, 2, 1, 80], [90, 85, 75, 65]]},
        {"grid": [[5, 5, 5], [5, 1, 5], [5, 5, 5]]},
        {"grid": [[-10, -20, -30], [-5, -15, -25], [-1, -2, -3], [-4, -6, -8]]},
        {"grid": [[9, 1, 8, 2, 7], [3, 6, 4, 5, 0], [12, 11, 10, 14, 13]]},
        {"grid": _rng_int_grid(5401, 11, 13, -100, 100)},
        {"grid": _rng_int_grid(5402, 25, 25, -5000, 5000)},
    ],
})

TASKS.append({
    "slug": "55-fill-matrix-in-anti-diagonal-order",
    "title": "Fill Matrix in Anti-Diagonal Order",
    "difficulty": "Easy",
    "subtopic": "Spiral Traversal",
    "companies": ["Amazon", "Microsoft", "Oracle"],
    "desc": (
        "Given two positive integers `rows` and `cols`, construct and return a `rows x cols` integer matrix filled "
        "with consecutive integers from `1` to `rows * cols` along its **anti-diagonals**.\n\n"
        "Anti-diagonals are ordered by increasing coordinate sum `d = r + c` for `d = 0, 1, ..., rows + cols - 2`. "
        "Within each anti-diagonal `d`, fill cells from **top-right to bottom-left** (that is, in increasing order "
        "of row index `r`)."
    ),
    "cons": [
        "1 <= rows, cols <= 100",
    ],
    "hints": [
        "Every cell on anti-diagonal d satisfies r + c = d, so c = d - r.",
        "For a fixed d, the valid row indices range from max(0, d - cols + 1) to min(rows - 1, d) inclusive.",
    ],
    "explanations": [
        "In a 3x3 matrix, anti-diagonal 0 fills (0,0)=1, anti-diagonal 1 fills (0,1)=2 and (1,0)=3, and so on down to (2,2)=9.",
        "In a 2x4 matrix, anti-diagonals have lengths 1, 2, 2, 2, 1 moving top-right to bottom-left.",
        "A 1x4 matrix has four length-1 anti-diagonals, producing [[1,2,3,4]].",
    ],
    "time": "O(rows * cols)",
    "space": "O(rows * cols)",
    "method": "fillAntiDiagonal",
    "params": [("rows", "int"), ("cols", "int")],
    "ret": "int[][]",
    "py": """        res = [[0] * cols for _ in range(rows)]
        val = 1
        for d in range(rows + cols - 1):
            r_start = max(0, d - cols + 1)
            r_end = min(rows - 1, d)
            for r in range(r_start, r_end + 1):
                res[r][d - r] = val
                val += 1
        return res""",
    "java": """        int[][] res = new int[rows][cols];
        int val = 1;
        for (int d = 0; d <= rows + cols - 2; d++) {
            int rStart = Math.max(0, d - cols + 1);
            int rEnd = Math.min(rows - 1, d);
            for (int r = rStart; r <= rEnd; r++) {
                res[r][d - r] = val++;
            }
        }
        return res;""",
    "visible": [
        {"rows": 3, "cols": 3},
        {"rows": 2, "cols": 4},
        {"rows": 1, "cols": 4},
    ],
    "hidden": [
        {"rows": 1, "cols": 1},
        {"rows": 4, "cols": 1},
        {"rows": 2, "cols": 2},
        {"rows": 4, "cols": 2},
        {"rows": 3, "cols": 5},
        {"rows": 5, "cols": 3},
        {"rows": 4, "cols": 4},
        {"rows": 10, "cols": 12},
        {"rows": 30, "cols": 30},
    ],
})

TASKS.append({
    "slug": "56-z-order-matrix-traversal",
    "title": "Z-Order Curve Matrix Traversal",
    "difficulty": "Medium",
    "subtopic": "Spiral Traversal",
    "companies": ["Google", "Meta", "Apple", "Uber"],
    "desc": (
        "You are given an `n x n` integer matrix `grid`, where `n` is guaranteed to be a power of `2` (`n = 2^k` "
        "for some integer `k >= 0`).\n\n"
        "Return a 1D integer array containing all elements of `grid` visited in recursive **Z-order (Morton curve)** "
        "traversal order:\n"
        "- If the current subgrid has size `1 x 1`, append its single element.\n"
        "- Otherwise, split the current `s x s` subgrid into four `(s / 2) x (s / 2)` quadrants and recursively "
        "traverse them in the exact order: **top-left**, **top-right**, **bottom-left**, **bottom-right**."
    ),
    "cons": [
        "n == grid.length == grid[i].length",
        "n is a power of 2 with 1 <= n <= 64.",
        "-10^6 <= grid[i][j] <= 10^6",
    ],
    "hints": [
        "Write a recursive helper traverse(r, c, size) that splits the square into four quadrants of side half = size // 2.",
        "Call the four quadrants in Z-order: (r, c), (r, c + half), (r + half, c), and (r + half, c + half).",
    ],
    "explanations": [
        "For a 2x2 grid, the four 1x1 quadrants are visited top-left (1), top-right (2), bottom-left (3), bottom-right (4).",
        "In a 4x4 grid, the top-left 2x2 block is fully traversed in Z-order [1,2,5,6], then top-right [3,4,7,8], bottom-left [9,10,13,14], and bottom-right [11,12,15,16].",
        "A 1x1 grid returns its sole element [7].",
    ],
    "time": "O(n^2)",
    "space": "O(n^2)",
    "method": "zOrderTraversal",
    "params": [("grid", "int[][]")],
    "ret": "int[]",
    "py": """        n = len(grid)
        res = []

        def dfs(r: int, c: int, size: int) -> None:
            if size == 1:
                res.append(grid[r][c])
                return
            h = size // 2
            dfs(r, c, h)
            dfs(r, c + h, h)
            dfs(r + h, c, h)
            dfs(r + h, c + h, h)

        dfs(0, 0, n)
        return res""",
    "java": """        int n = grid.length;
        int[] res = new int[n * n];
        int[] idx = new int[1];
        dfs(grid, 0, 0, n, res, idx);
        return res;""",
    "java_helpers": """    private void dfs(int[][] grid, int r, int c, int size, int[] res, int[] idx) {
        if (size == 1) {
            res[idx[0]++] = grid[r][c];
            return;
        }
        int h = size / 2;
        dfs(grid, r, c, h, res, idx);
        dfs(grid, r, c + h, h, res, idx);
        dfs(grid, r + h, c, h, res, idx);
        dfs(grid, r + h, c + h, h, res, idx);
    }""",
    "visible": [
        {"grid": [[1, 2], [3, 4]]},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]},
        {"grid": [[7]]},
    ],
    "hidden": [
        {"grid": [[-5]]},
        {"grid": [[10, 20], [30, 40]]},
        {"grid": [[0, 0], [0, 0]]},
        {"grid": [[-1, -2, -3, -4], [-5, -6, -7, -8], [-9, -10, -11, -12], [-13, -14, -15, -16]]},
        {"grid": _rng_int_grid(5601, 4, 4, -50, 50)},
        {"grid": [[r * 8 + c for c in range(8)] for r in range(8)]},
        {"grid": _rng_int_grid(5602, 8, 8, -1000, 1000)},
        {"grid": _rng_int_grid(5603, 16, 16, -10000, 10000)},
        {"grid": _rng_int_grid(5604, 32, 32, -100000, 100000)},
    ],
})

TASKS.append({
    "slug": "57-maximum-subarray-along-spiral-order",
    "title": "Maximum Subarray Sum Along Spiral Order",
    "difficulty": "Medium",
    "subtopic": "Spiral Traversal",
    "companies": ["Amazon", "Google", "Meta", "Goldman Sachs"],
    "desc": (
        "You are given an `m x n` integer matrix `matrix` whose cells may contain positive, zero, or negative values.\n\n"
        "Consider the 1D sequence formed by traversing `matrix` in standard **clockwise spiral order** starting at "
        "`(0, 0)` (right across the top row, down the right column, left across the bottom row, up the left column, "
        "and repeating inward).\n\n"
        "Return the **maximum sum** of a non-empty contiguous subarray within this spiral sequence (wrap-around is "
        "not allowed). Try to solve it in `O(1)` extra space without materializing the 1D array."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 200",
        "-10^4 <= matrix[i][j] <= 10^4",
    ],
    "hints": [
        "Maintain the four shrinking spiral boundaries (top, bottom, left, right) just as in standard spiral traversal.",
        "Feed each visited element directly into Kadane's algorithm (cur = max(val, cur + val); best = max(best, cur)), ensuring you handle all-negative matrices correctly.",
    ],
    "explanations": [
        "The clockwise spiral order is [1, -2, 3, 4, 5, -1, 2, -6, 10]; the contiguous segment [3, 4, 5, -1, 2, -6, 10] has maximum sum 17.",
        "All entries are negative, so the best non-empty subarray along the spiral is the single largest element -2.",
        "The spiral order is [2, 3, -10, 4, 5, 1]; the contiguous segment [4, 5, 1] yields sum 10.",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "maxSpiralSubarraySum",
    "params": [("matrix", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(matrix), len(matrix[0])
        top, bottom, left, right = 0, m - 1, 0, n - 1
        started = False
        cur = 0
        best = 0

        def visit(v: int) -> None:
            nonlocal started, cur, best
            if not started:
                cur = best = v
                started = True
            else:
                cur = v if cur < 0 else cur + v
                if cur > best:
                    best = cur

        while top <= bottom and left <= right:
            for c in range(left, right + 1):
                visit(matrix[top][c])
            top += 1
            for r in range(top, bottom + 1):
                visit(matrix[r][right])
            right -= 1
            if top <= bottom:
                for c in range(right, left - 1, -1):
                    visit(matrix[bottom][c])
                bottom -= 1
            if left <= right:
                for r in range(bottom, top - 1, -1):
                    visit(matrix[r][left])
                left += 1
        return best""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        int top = 0, bottom = m - 1, left = 0, right = n - 1;
        boolean started = false;
        int cur = 0, best = Integer.MIN_VALUE;
        while (top <= bottom && left <= right) {
            for (int c = left; c <= right; c++) {
                int v = matrix[top][c];
                cur = started ? Math.max(v, cur + v) : v;
                started = true;
                if (cur > best) best = cur;
            }
            top++;
            for (int r = top; r <= bottom; r++) {
                int v = matrix[r][right];
                cur = started ? Math.max(v, cur + v) : v;
                started = true;
                if (cur > best) best = cur;
            }
            right--;
            if (top <= bottom) {
                for (int c = right; c >= left; c--) {
                    int v = matrix[bottom][c];
                    cur = started ? Math.max(v, cur + v) : v;
                    started = true;
                    if (cur > best) best = cur;
                }
                bottom--;
            }
            if (left <= right) {
                for (int r = bottom; r >= top; r--) {
                    int v = matrix[r][left];
                    cur = started ? Math.max(v, cur + v) : v;
                    started = true;
                    if (cur > best) best = cur;
                }
                left++;
            }
        }
        return best;""",
    "visible": [
        {"matrix": [[1, -2, 3], [-6, 10, 4], [2, -1, 5]]},
        {"matrix": [[-5, -3], [-2, -8]]},
        {"matrix": [[2, 3, -10], [1, 5, 4]]},
    ],
    "hidden": [
        {"matrix": [[-100]]},
        {"matrix": [[0]]},
        {"matrix": [[5, -1, 3, -2, 4]]},
        {"matrix": [[3], [-4], [2], [5], [-1]]},
        {"matrix": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]},
        {"matrix": [[-1, 5, -1], [-1, -10, 5], [5, -1, 5]]},
        {"matrix": [[4, -10, 3, 2], [1, 8, -2, 5], [-3, 6, -1, 4], [7, -5, 2, -6]]},
        {"matrix": _rng_int_grid(5701, 15, 18, -30, 30)},
        {"matrix": _rng_int_grid(5702, 35, 35, -100, 95)},
    ],
})

TASKS.append({
    "slug": "58-spiral-walk-with-obstacles",
    "title": "Spiral Walk with Obstacles",
    "difficulty": "Medium",
    "subtopic": "Spiral Traversal",
    "companies": ["Amazon", "Uber", "Microsoft", "Atlassian"],
    "desc": (
        "You are given an `m x n` integer matrix `grid`, where `grid[r][c] >= 0` represents a passable cell with a "
        "value and `grid[r][c] == -1` represents an impassable obstacle. The starting cell `(0, 0)` is guaranteed "
        "to be passable (`grid[0][0] >= 0`).\n\n"
        "A robot starts at `(0, 0)` facing **Right** (East), records `grid[0][0]`, and marks `(0, 0)` as visited. "
        "At each step, the robot tries to move one cell forward in its current direction. If the target cell is "
        "out of bounds, an obstacle (`-1`), or already visited, the robot rotates 90 degrees clockwise "
        "(`Right -> Down -> Left -> Up -> Right`) and checks again, repeating up to 3 rotations. It moves into the "
        "first valid unvisited passable cell found, updates its facing direction accordingly, marks that cell visited, "
        "and records its value. If all four directions are blocked or already visited, the robot halts.\n\n"
        "Return an integer array of all recorded values in the exact order the robot visited them."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 100",
        "-1 <= grid[i][j] <= 10^4",
        "grid[0][0] >= 0",
    ],
    "hints": [
        "Store the four clockwise direction vectors [(0, 1), (1, 0), (0, -1), (-1, 0)] and track a visited boolean matrix.",
        "From the current cell and direction d, try offsets k = 0, 1, 2, 3 using nd = (d + k) % 4; take the first valid unvisited open cell, or terminate if none exists.",
    ],
    "explanations": [
        "Starting at (0,0)=1 facing right, the robot visits 2, hits the obstacle at (0,2), turns down to 5, hits bottom, turns left to 4, turns up? (0,0) is visited, so it halts after [1,2,5,4]? Wait: at (1,1)=5 it goes down to (2,1)=8, turns left to (2,0)=7, turns up to (1,0)=4, and stops with [1,2,5,8,7,4].",
        "With obstacles blocking both right and down from (0,0), the robot cannot move and returns [9].",
        "With no obstacles, the robot performs a standard full clockwise spiral returning [1,2,3,6,5,4].",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "spiralWalkWithObstacles",
    "params": [("grid", "int[][]")],
    "ret": "int[]",
    "py": """        m, n = len(grid), len(grid[0])
        dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
        vis = [[False] * n for _ in range(m)]
        r = c = d = 0
        vis[0][0] = True
        ans = [grid[0][0]]
        while True:
            moved = False
            for k in range(4):
                nd = (d + k) % 4
                nr = r + dirs[nd][0]
                nc = c + dirs[nd][1]
                if 0 <= nr < m and 0 <= nc < n and not vis[nr][nc] and grid[nr][nc] != -1:
                    r, c, d = nr, nc, nd
                    vis[r][c] = True
                    ans.append(grid[r][c])
                    moved = True
                    break
            if not moved:
                break
        return ans""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[][] dirs = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        boolean[][] vis = new boolean[m][n];
        int r = 0, c = 0, d = 0;
        vis[0][0] = true;
        List<Integer> list = new ArrayList<>();
        list.add(grid[0][0]);
        while (true) {
            boolean moved = false;
            for (int k = 0; k < 4; k++) {
                int nd = (d + k) % 4;
                int nr = r + dirs[nd][0];
                int nc = c + dirs[nd][1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && !vis[nr][nc] && grid[nr][nc] != -1) {
                    r = nr;
                    c = nc;
                    d = nd;
                    vis[r][c] = true;
                    list.add(grid[r][c]);
                    moved = true;
                    break;
                }
            }
            if (!moved) break;
        }
        int[] ans = new int[list.size()];
        for (int i = 0; i < list.size(); i++) ans[i] = list.get(i);
        return ans;""",
    "visible": [
        {"grid": [[1, 2, -1], [4, 5, 6], [7, 8, 9]]},
        {"grid": [[9, -1], [-1, 4]]},
        {"grid": [[1, 2, 3], [4, 5, 6]]},
    ],
    "hidden": [
        {"grid": [[0]]},
        {"grid": [[1, 2, 3, -1, 5]]},
        {"grid": [[1], [2], [-1], [4]]},
        {"grid": [[1, 2, 3, 4], [5, -1, -1, 8], [9, 10, 11, 12]]},
        {"grid": [[1, -1, 3], [2, 4, 5], [6, 7, 8]]},
        {"grid": [[10, 20, 30, 40], [50, 60, -1, 80], [90, 100, 110, 120], [130, 140, 150, 160]]},
        {"grid": [[5, 6, 7], [-1, 8, -1], [1, 2, 3]]},
        {"grid": _rng_obstacle_grid(5801, 12, 12, 0.2)},
        {"grid": _rng_obstacle_grid(5802, 30, 30, 0.12)},
    ],
})

# Fix visible explanation #1 for problem 58 so there is no draft note inside the explanation text!
TASKS[-1]["explanations"][0] = (
    "Starting at (0,0)=1 facing right, the robot visits 2, hits the obstacle at (0,2), turns down through 5 and 8, "
    "turns left to 7, turns up to 4, and halts because every neighbor of (1,0) is visited or out of bounds."
)

TASKS.append({
    "slug": "59-diagonal-difference-of-distinct-values",
    "title": "Difference of Distinct Values on Diagonals",
    "difficulty": "Easy",
    "subtopic": "Spiral Traversal",
    "companies": ["Google", "Amazon", "Adobe"],
    "desc": (
        "Given a 0-indexed `m x n` integer matrix `grid`, return an `m x n` integer matrix `answer` where:\n\n"
        "`answer[r][c] = |topLeft[r][c] - bottomRight[r][c]|`\n\n"
        "Here:\n"
        "- `topLeft[r][c]` is the number of **distinct** values strictly on the top-left main diagonal of `(r, c)`, "
        "consisting of all in-bounds cells `(r - k, c - k)` with `k >= 1`.\n"
        "- `bottomRight[r][c]` is the number of **distinct** values strictly on the bottom-right main diagonal of "
        "`(r, c)`, consisting of all in-bounds cells `(r + k, c + k)` with `k >= 1`."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 50",
        "1 <= grid[i][j] <= 10^5",
    ],
    "hints": [
        "Walk each main diagonal (cells sharing the same r - c) independently from top-left to bottom-right while maintaining a hash set of seen values to fill topLeft counts in O(1) per cell.",
        "Then walk each diagonal in reverse (bottom-right to top-left) with a fresh hash set to compute bottomRight counts and take the absolute difference.",
    ],
    "explanations": [
        "For (0,0), topLeft has 0 distinct values and bottomRight has {1} (1 distinct), giving |0 - 1| = 1; similarly every other cell is evaluated along its main diagonal.",
        "In a 1x1 matrix both diagonal halves are empty, so answer is [[0]].",
        "In a single row, every cell has empty top-left and bottom-right diagonals, so every entry is 0.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "differenceOfDistinctValues",
    "params": [("grid", "int[][]")],
    "ret": "int[][]",
    "py": """        m, n = len(grid), len(grid[0])
        ans = [[0] * n for _ in range(m)]
        starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
        for sr, sc in starts:
            cells = []
            r, c = sr, sc
            seen = set()
            while r < m and c < n:
                ans[r][c] = len(seen)
                seen.add(grid[r][c])
                cells.append((r, c))
                r += 1
                c += 1
            seen.clear()
            for r, c in reversed(cells):
                ans[r][c] = abs(ans[r][c] - len(seen))
                seen.add(grid[r][c])
        return ans""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[][] ans = new int[m][n];
        for (int start = -(m - 1); start <= n - 1; start++) {
            int r = Math.max(0, -start);
            int c = Math.max(0, start);
            List<int[]> cells = new ArrayList<>();
            Set<Integer> seen = new HashSet<>();
            while (r < m && c < n) {
                ans[r][c] = seen.size();
                seen.add(grid[r][c]);
                cells.add(new int[]{r, c});
                r++;
                c++;
            }
            seen.clear();
            for (int i = cells.size() - 1; i >= 0; i--) {
                int cr = cells.get(i)[0], cc = cells.get(i)[1];
                ans[cr][cc] = Math.abs(ans[cr][cc] - seen.size());
                seen.add(grid[cr][cc]);
            }
        }
        return ans;""",
    "visible": [
        {"grid": [[1, 2, 3], [3, 1, 5], [3, 2, 1]]},
        {"grid": [[1]]},
        {"grid": [[5, 5, 5]]},
    ],
    "hidden": [
        {"grid": [[1], [2], [3]]},
        {"grid": [[1, 1], [1, 1]]},
        {"grid": [[1, 2], [3, 4]]},
        {"grid": [[7, 7, 7], [7, 7, 7], [7, 7, 7]]},
        {"grid": [[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]]},
        {"grid": [[10, 20], [30, 10], [40, 50], [60, 10]]},
        {"grid": [[1, 2, 1, 2], [2, 1, 2, 1], [1, 2, 1, 2], [2, 1, 2, 1]]},
        {"grid": _rng_int_grid(5901, 15, 15, 1, 10)},
        {"grid": _rng_int_grid(5902, 35, 35, 1, 20)},
    ],
})

# ============================================================================
# Subtopic 2: Matrix Rotation (60 - 65)
# ============================================================================

TASKS.append({
    "slug": "60-score-after-flipping-matrix",
    "title": "Score After Flipping Binary Matrix",
    "difficulty": "Medium",
    "subtopic": "Matrix Rotation",
    "companies": ["Google", "Amazon", "Meta", "Microsoft"],
    "desc": (
        "You are given an `m x n` binary matrix `grid` containing only `0`s and `1`s.\n\n"
        "A **move** consists of choosing any row or any column and toggling every value in that row or column "
        "(changing every `0` to `1` and every `1` to `0`).\n\n"
        "After performing any number of moves, every row of the matrix is interpreted as a binary number (with "
        "column `0` as the most significant bit), and the score of the matrix is the sum of these `m` numbers.\n\n"
        "Return the **highest possible score** achievable."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 20",
        "grid[i][j] is either 0 or 1.",
    ],
    "hints": [
        "The most significant bit (column 0) outweighs all remaining bits combined, so greedily toggle any row whose first entry is 0 so that column 0 becomes all 1s.",
        "Once row orientations are fixed, maximize each remaining column c independently by counting how many rows have grid[r][c] == grid[r][0] (the effective 1s) and taking max(ones, m - ones).",
    ],
    "explanations": [
        "Flipping row 0, then column 2, then column 3 produces rows 1111 (15), 1001 (9), and 1111 (15), totaling 39.",
        "Flipping the single 0 to 1 gives a score of 1.",
        "All entries are already 1 in a 2x2 grid (11 + 11 = 3 + 3 = 6), which is optimal.",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "matrixScore",
    "params": [("grid", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(grid), len(grid[0])
        score = m * (1 << (n - 1))
        for c in range(1, n):
            same = sum(1 for r in range(m) if grid[r][c] == grid[r][0])
            score += max(same, m - same) * (1 << (n - 1 - c))
        return score""",
    "java": """        int m = grid.length, n = grid[0].length;
        int score = m * (1 << (n - 1));
        for (int c = 1; c < n; c++) {
            int same = 0;
            for (int r = 0; r < m; r++) {
                if (grid[r][c] == grid[r][0]) same++;
            }
            score += Math.max(same, m - same) * (1 << (n - 1 - c));
        }
        return score;""",
    "visible": [
        {"grid": [[0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0]]},
        {"grid": [[0]]},
        {"grid": [[1, 1], [1, 1]]},
    ],
    "hidden": [
        {"grid": [[1]]},
        {"grid": [[0, 0, 0]]},
        {"grid": [[0], [1], [0], [1]]},
        {"grid": [[0, 1], [1, 0]]},
        {"grid": [[1, 0, 0], [0, 1, 1], [0, 0, 1]]},
        {"grid": [[0, 1, 0, 1, 0], [1, 0, 1, 0, 1], [0, 0, 1, 1, 0]]},
        {"grid": _rng_bin_grid(6001, 10, 10, 0.5)},
        {"grid": _rng_bin_grid(6002, 18, 16, 0.35)},
        {"grid": _rng_bin_grid(6003, 20, 20, 0.5)},
    ],
})

TASKS.append({
    "slug": "61-flip-columns-for-maximum-equal-rows",
    "title": "Flip Columns for Maximum Equal Rows",
    "difficulty": "Medium",
    "subtopic": "Matrix Rotation",
    "companies": ["Google", "Amazon", "Meta", "Bloomberg"],
    "desc": (
        "You are given an `m x n` binary matrix `matrix` containing only `0`s and `1`s.\n\n"
        "You may choose any number of columns (including zero) and flip every cell in those chosen columns "
        "(changing `0` to `1` and `1` to `0`).\n\n"
        "Return the **maximum number of rows** that have all values equal (either all `0`s or all `1`s) after "
        "applying an optimal subset of column flips."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 200",
        "matrix[i][j] is either 0 or 1.",
    ],
    "hints": [
        "Two rows can simultaneously become all-equal after the same subset of column flips if and only if they are identical or exact bitwise complements of each other.",
        "Canonicalize every row by flipping all its bits whenever row[0] == 1, then count the frequency of each canonical pattern with a hash map.",
    ],
    "explanations": [
        "No matter which columns are flipped, at most 1 row can have all equal values (rows [0,1] and [1,1] are neither equal nor complements).",
        "Flipping column 0 turns [0,1] into [1,1] and [1,0] into [0,0], giving 2 all-equal rows.",
        "Flipping column 0 makes rows 1 and 2 all-equal ([1,1,1] and [0,0,0]), giving 2 rows.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "maxEqualRowsAfterFlips",
    "params": [("matrix", "int[][]")],
    "ret": "int",
    "py": """        counts = Counter()
        for row in matrix:
            first = row[0]
            pattern = tuple(v ^ first for v in row)
            counts[pattern] += 1
        return max(counts.values())""",
    "java": """        Map<String, Integer> counts = new HashMap<>();
        int best = 0;
        for (int[] row : matrix) {
            int first = row[0];
            char[] key = new char[row.length];
            for (int c = 0; c < row.length; c++) {
                key[c] = (row[c] == first) ? '0' : '1';
            }
            String s = new String(key);
            int cnt = counts.getOrDefault(s, 0) + 1;
            counts.put(s, cnt);
            if (cnt > best) best = cnt;
        }
        return best;""",
    "visible": [
        {"matrix": [[0, 1], [1, 1]]},
        {"matrix": [[0, 1], [1, 0]]},
        {"matrix": [[0, 0, 0], [0, 0, 1], [1, 1, 0]]},
    ],
    "hidden": [
        {"matrix": [[0]]},
        {"matrix": [[1], [0], [1], [0]]},
        {"matrix": [[1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1]]},
        {"matrix": [[0, 0, 0], [1, 1, 1], [0, 0, 0]]},
        {"matrix": [[1, 0, 0, 1], [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1]]},
        {"matrix": [[0, 1, 0, 0, 1], [1, 0, 1, 1, 0], [0, 1, 1, 0, 1], [1, 0, 0, 1, 0], [0, 1, 0, 0, 1]]},
        {"matrix": _rng_bin_grid(6101, 20, 4, 0.5)},
        {"matrix": _rng_bin_grid(6102, 50, 6, 0.5)},
        {"matrix": _rng_bin_grid(6103, 80, 12, 0.5)},
    ],
})

TASKS.append({
    "slug": "62-minimum-flips-for-full-grid-palindromes",
    "title": "Minimum Flips for Palindromic Grid II",
    "difficulty": "Hard",
    "subtopic": "Matrix Rotation",
    "companies": ["Google", "Meta", "Amazon", "Apple"],
    "desc": (
        "You are given an `m x n` binary matrix `grid` containing only `0`s and `1`s.\n\n"
        "In a single operation, you can flip any cell (`0` to `1`, or `1` to `0`). Return the **minimum number of "
        "flips** required so that ALL of the following conditions hold simultaneously:\n"
        "1. Every **row** is palindromic.\n"
        "2. Every **column** is palindromic.\n"
        "3. The **total number of `1`s** in the entire grid is divisible by `4`."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 200",
        "grid[i][j] is either 0 or 1.",
    ],
    "hints": [
        "Every non-middle cell (r, c) belongs to a 4-cell symmetry orbit {(r, c), (r, n-1-c), (m-1-r, c), (m-1-r, n-1-c)} that must all share the same value (contributing 0 or 4 ones), costing min(ones, 4 - ones).",
        "Handle the middle row (when m is odd), middle column (when n is odd), and the single center cell (which must be 0 when both m and n are odd): if the number of (1, 1) symmetric pairs is odd and there are no differing (0, 1) pairs to absorb the parity adjustment, add 2 extra flips.",
    ],
    "explanations": [
        "Flipping (0,0), (1,1), and (2,2) leaves all zeros (0 is divisible by 4) in 3 flips, which is optimal.",
        "Flipping (0,0) and (2,0) to 0 makes all rows and columns palindromic with 0 ones in 2 flips (flipping (1,0) would leave 3 ones, not divisible by 4).",
        "Flipping the single 1 in the 1x1 grid to 0 makes total ones equal to 0 (divisible by 4) in 1 flip.",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "minFlipsFullPalindrome",
    "params": [("grid", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(grid), len(grid[0])
        flips = 0
        for r in range(m // 2):
            for c in range(n // 2):
                ones = (
                    grid[r][c]
                    + grid[r][n - 1 - c]
                    + grid[m - 1 - r][c]
                    + grid[m - 1 - r][n - 1 - c]
                )
                flips += min(ones, 4 - ones)

        diff = 0
        pair_ones = 0
        if m % 2 == 1:
            mr = m // 2
            for c in range(n // 2):
                a, b = grid[mr][c], grid[mr][n - 1 - c]
                if a != b:
                    diff += 1
                elif a == 1:
                    pair_ones += 1
        if n % 2 == 1:
            mc = n // 2
            for r in range(m // 2):
                a, b = grid[r][mc], grid[m - 1 - r][mc]
                if a != b:
                    diff += 1
                elif a == 1:
                    pair_ones += 1
        if m % 2 == 1 and n % 2 == 1 and grid[m // 2][n // 2] == 1:
            flips += 1

        flips += diff
        if pair_ones % 2 == 1 and diff == 0:
            flips += 2
        return flips""",
    "java": """        int m = grid.length, n = grid[0].length;
        int flips = 0;
        for (int r = 0; r < m / 2; r++) {
            for (int c = 0; c < n / 2; c++) {
                int ones = grid[r][c]
                        + grid[r][n - 1 - c]
                        + grid[m - 1 - r][c]
                        + grid[m - 1 - r][n - 1 - c];
                flips += Math.min(ones, 4 - ones);
            }
        }
        int diff = 0, pairOnes = 0;
        if (m % 2 == 1) {
            int mr = m / 2;
            for (int c = 0; c < n / 2; c++) {
                int a = grid[mr][c], b = grid[mr][n - 1 - c];
                if (a != b) diff++;
                else if (a == 1) pairOnes++;
            }
        }
        if (n % 2 == 1) {
            int mc = n / 2;
            for (int r = 0; r < m / 2; r++) {
                int a = grid[r][mc], b = grid[m - 1 - r][mc];
                if (a != b) diff++;
                else if (a == 1) pairOnes++;
            }
        }
        if (m % 2 == 1 && n % 2 == 1 && grid[m / 2][n / 2] == 1) {
            flips++;
        }
        flips += diff;
        if (pairOnes % 2 == 1 && diff == 0) {
            flips += 2;
        }
        return flips;""",
    "visible": [
        {"grid": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
        {"grid": [[1], [0], [1]]},
        {"grid": [[1]]},
    ],
    "hidden": [
        {"grid": [[0]]},
        {"grid": [[1, 1], [1, 1]]},
        {"grid": [[1, 0], [0, 1]]},
        {"grid": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]},
        {"grid": [[0, 1], [0, 1], [0, 0]]},
        {"grid": [[1, 1, 0, 1, 1]]},
        {"grid": [[1, 0, 1, 0, 1], [0, 1, 1, 1, 0], [1, 1, 0, 1, 1]]},
        {"grid": _rng_bin_grid(6201, 15, 17, 0.55)},
        {"grid": _rng_bin_grid(6202, 35, 35, 0.5)},
    ],
})

TASKS.append({
    "slug": "63-check-rotational-symmetry-matrix",
    "title": "Check Matrix Rotational Symmetry",
    "difficulty": "Easy",
    "subtopic": "Matrix Rotation",
    "companies": ["Amazon", "Apple", "Adobe"],
    "desc": (
        "Given an `m x n` integer matrix `grid`, determine whether `grid` has **180-degree rotational symmetry** "
        "(also known as central point symmetry).\n\n"
        "A matrix has 180-degree rotational symmetry if rotating the entire matrix by 180 degrees leaves every "
        "cell's value unchanged—equivalently, `grid[r][c] == grid[m - 1 - r][n - 1 - c]` for every `0 <= r < m` "
        "and `0 <= c < n`. Return `true` if `grid` is rotationally symmetric, otherwise `false`."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 200",
        "-10^6 <= grid[i][j] <= 10^6",
    ],
    "hints": [
        "Under a 180-degree rotation, cell (r, c) maps to (m - 1 - r, n - 1 - c).",
        "You only need to check the first half of rows (and the first half of the middle row if m is odd), returning false on the first mismatch.",
    ],
    "explanations": [
        "Rotating [[1,2,3],[4,5,4],[3,2,1]] by 180 degrees produces the exact same matrix.",
        "Cell (0,0) is 1 while its 180-degree opposite (1,1) is 2, so the matrix is not rotationally symmetric.",
        "Every 1x1 matrix is trivially invariant under a 180-degree rotation.",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "hasRotationalSymmetry",
    "params": [("grid", "int[][]")],
    "ret": "boolean",
    "py": """        m, n = len(grid), len(grid[0])
        for r in range((m + 1) // 2):
            mr = m - 1 - r
            col_limit = (n + 1) // 2 if r == mr else n
            for c in range(col_limit):
                if grid[r][c] != grid[mr][n - 1 - c]:
                    return False
        return True""",
    "java": """        int m = grid.length, n = grid[0].length;
        for (int r = 0; r < (m + 1) / 2; r++) {
            int mr = m - 1 - r;
            int colLimit = (r == mr) ? (n + 1) / 2 : n;
            for (int c = 0; c < colLimit; c++) {
                if (grid[r][c] != grid[mr][n - 1 - c]) return false;
            }
        }
        return true;""",
    "visible": [
        {"grid": [[1, 2, 3], [4, 5, 4], [3, 2, 1]]},
        {"grid": [[1, 2], [1, 2]]},
        {"grid": [[9]]},
    ],
    "hidden": [
        {"grid": [[1, 2, 3, 2, 1]]},
        {"grid": [[1, 2, 3, 4]]},
        {"grid": [[7], [8], [7]]},
        {"grid": [[1, 2], [2, 1]]},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [8, 7, 6, 5], [4, 3, 2, 1]]},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [8, 7, 6, 5], [4, 3, 9, 1]]},
        {"grid": [[-5, 0, 5], [0, 99, 0], [5, 0, -5]]},
        {
            "grid": [
                [(r * 17 + c * 31) % 50 if r < 15 else ((29 - r) * 17 + (29 - c) * 31) % 50 for c in range(30)]
                for r in range(30)
            ]
        },
        {"grid": _rng_int_grid(6301, 30, 30, -100, 100)},
    ],
})

TASKS.append({
    "slug": "64-rotate-square-submatrix-clockwise",
    "title": "Rotate Square Submatrix Clockwise",
    "difficulty": "Medium",
    "subtopic": "Matrix Rotation",
    "companies": ["Amazon", "Microsoft", "Apple", "Uber"],
    "desc": (
        "You are given an `m x n` integer matrix `grid`, integers `row`, `col`, `k`, and `turns`.\n\n"
        "Consider the `k x k` contiguous square submatrix whose top-left corner is at `(row, col)` (covering rows "
        "`row .. row + k - 1` and columns `col .. col + k - 1`). Rotate **only** this `k x k` submatrix clockwise "
        "by `90` degrees exactly `turns` times, while leaving every cell outside the submatrix unchanged.\n\n"
        "Return the resulting `m x n` integer matrix."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 100",
        "1 <= k <= min(m, n)",
        "0 <= row <= m - k and 0 <= col <= n - k",
        "0 <= turns <= 10^9",
        "-10^5 <= grid[i][j] <= 10^5",
    ],
    "hints": [
        "Four 90-degree rotations return the submatrix to its original orientation, so first reduce t = turns % 4.",
        "Copy the grid and map each relative offset (dr, dc) inside the k x k window directly to its target position based on t in {0, 1, 2, 3}.",
    ],
    "explanations": [
        "The bottom-right 2x2 submatrix [[5,6],[8,9]] rotates 90 degrees clockwise into [[8,5],[9,6]], leaving row 0 and column 0 untouched.",
        "Rotating the entire 2x2 matrix twice (180 degrees) reverses both rows and columns.",
        "Because 4 turns is a full 360-degree rotation, the matrix remains completely unchanged.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "rotateSubmatrix",
    "params": [("grid", "int[][]"), ("row", "int"), ("col", "int"), ("k", "int"), ("turns", "int")],
    "ret": "int[][]",
    "py": """        res = [r[:] for r in grid]
        t = turns % 4
        if t == 0 or k == 1:
            return res
        for dr in range(k):
            for dc in range(k):
                val = grid[row + dr][col + dc]
                if t == 1:
                    res[row + dc][col + k - 1 - dr] = val
                elif t == 2:
                    res[row + k - 1 - dr][col + k - 1 - dc] = val
                else:
                    res[row + k - 1 - dc][col + dr] = val
        return res""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        for (int r = 0; r < m; r++) res[r] = grid[r].clone();
        int t = turns % 4;
        if (t == 0 || k == 1) return res;
        for (int dr = 0; dr < k; dr++) {
            for (int dc = 0; dc < k; dc++) {
                int val = grid[row + dr][col + dc];
                if (t == 1) {
                    res[row + dc][col + k - 1 - dr] = val;
                } else if (t == 2) {
                    res[row + k - 1 - dr][col + k - 1 - dc] = val;
                } else {
                    res[row + k - 1 - dc][col + dr] = val;
                }
            }
        }
        return res;""",
    "visible": [
        {"grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "row": 1, "col": 1, "k": 2, "turns": 1},
        {"grid": [[1, 2], [3, 4]], "row": 0, "col": 0, "k": 2, "turns": 2},
        {"grid": [[10, 20, 30], [40, 50, 60]], "row": 0, "col": 1, "k": 2, "turns": 4},
    ],
    "hidden": [
        {"grid": [[7]], "row": 0, "col": 0, "k": 1, "turns": 1000000000},
        {"grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "row": 0, "col": 0, "k": 3, "turns": 3},
        {"grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "row": 0, "col": 0, "k": 3, "turns": 0},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], "row": 1, "col": 1, "k": 3, "turns": 999999999},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], "row": 0, "col": 1, "k": 3, "turns": 1},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]], "row": 0, "col": 1, "k": 3, "turns": 2},
        {"grid": [[-1, -2, -3], [-4, -5, -6], [-7, -8, -9]], "row": 0, "col": 0, "k": 2, "turns": 7},
        {"grid": _rng_int_grid(6401, 15, 18, -50, 50), "row": 3, "col": 4, "k": 10, "turns": 100000001},
        {"grid": _rng_int_grid(6402, 30, 30, -1000, 1000), "row": 5, "col": 5, "k": 20, "turns": 987654323},
    ],
})

TASKS.append({
    "slug": "65-transform-to-chessboard",
    "title": "Minimum Swaps to Form Chessboard",
    "difficulty": "Hard",
    "subtopic": "Matrix Rotation",
    "companies": ["Google", "Meta", "Goldman Sachs", "Amazon"],
    "desc": (
        "You are given an `n x n` binary grid `board`. In each move, you can swap any two rows with each other, "
        "or swap any two columns with each other.\n\n"
        "Return the **minimum number of moves** required to transform `board` into a valid **chessboard**—a board "
        "where no two horizontally or vertically adjacent cells have the same value (`0` or `1`). If it is "
        "impossible to transform `board` into a chessboard, return `-1`."
    ),
    "cons": [
        "n == board.length == board[i].length",
        "2 <= n <= 30",
        "board[i][j] is either 0 or 1.",
    ],
    "hints": [
        "Row and column swaps preserve the rectangle parity invariant: for every (r, c), board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c] must equal 0 (meaning every row equals row 0 or its bitwise complement).",
        "Verify that both the first row and first column have either floor(n/2) or ceil(n/2) ones; then count misaligned rows and columns independently to find the minimum swaps.",
    ],
    "explanations": [
        "Swap columns 0 and 1, then swap rows 1 and 2 to obtain a valid 4x4 chessboard in 2 moves.",
        "The 2x2 board is already a valid chessboard, requiring 0 moves.",
        "Row 0 has [1,0] while row 1 has [1,1], which violates the complement invariant, so no chessboard is possible (-1).",
    ],
    "time": "O(n^2)",
    "space": "O(1)",
    "method": "movesToChessboard",
    "params": [("board", "int[][]")],
    "ret": "int",
    "py": """        n = len(board)
        for r in range(n):
            for c in range(n):
                if (board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c]) != 0:
                    return -1

        row_sum = col_sum = row_swap = col_swap = 0
        for i in range(n):
            row_sum += board[0][i]
            col_sum += board[i][0]
            if board[i][0] == i % 2:
                row_swap += 1
            if board[0][i] == i % 2:
                col_swap += 1

        if row_sum != n // 2 and row_sum != (n + 1) // 2:
            return -1
        if col_sum != n // 2 and col_sum != (n + 1) // 2:
            return -1

        if n % 2 == 1:
            if row_swap % 2 == 1:
                row_swap = n - row_swap
            if col_swap % 2 == 1:
                col_swap = n - col_swap
        else:
            row_swap = min(row_swap, n - row_swap)
            col_swap = min(col_swap, n - col_swap)
        return (row_swap + col_swap) // 2""",
    "java": """        int n = board.length;
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                if ((board[0][0] ^ board[r][0] ^ board[0][c] ^ board[r][c]) != 0) {
                    return -1;
                }
            }
        }
        int rowSum = 0, colSum = 0, rowSwap = 0, colSwap = 0;
        for (int i = 0; i < n; i++) {
            rowSum += board[0][i];
            colSum += board[i][0];
            if (board[i][0] == i % 2) rowSwap++;
            if (board[0][i] == i % 2) colSwap++;
        }
        if (rowSum != n / 2 && rowSum != (n + 1) / 2) return -1;
        if (colSum != n / 2 && colSum != (n + 1) / 2) return -1;
        if (n % 2 == 1) {
            if (rowSwap % 2 == 1) rowSwap = n - rowSwap;
            if (colSwap % 2 == 1) colSwap = n - colSwap;
        } else {
            rowSwap = Math.min(rowSwap, n - rowSwap);
            colSwap = Math.min(colSwap, n - colSwap);
        }
        return (rowSwap + colSwap) / 2;""",
    "visible": [
        {"board": [[0, 1, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1], [1, 0, 0, 1]]},
        {"board": [[0, 1], [1, 0]]},
        {"board": [[1, 0], [1, 1]]},
    ],
    "hidden": [
        {"board": [[1, 0], [0, 1]]},
        {"board": [[0, 0], [1, 1]]},
        {"board": [[0, 1, 0], [1, 0, 1], [0, 1, 0]]},
        {"board": [[1, 0, 1], [1, 0, 1], [0, 1, 0]]},
        {"board": [[1, 1, 0], [0, 0, 1], [0, 0, 1]]},
        {"board": [[1, 0, 0, 1, 1], [0, 1, 1, 0, 0], [1, 0, 0, 1, 1], [0, 1, 1, 0, 0], [0, 1, 1, 0, 0]]},
        {"board": _rng_chessboard(6501, 11, valid=True)},
        {"board": _rng_chessboard(6502, 20, valid=False)},
        {"board": _rng_chessboard(6503, 30, valid=True)},
    ],
})

# ============================================================================
# Subtopic 3: 2D Search (66 - 71)
# ============================================================================

TASKS.append({
    "slug": "66-maximum-side-length-of-square-with-sum-threshold",
    "title": "Maximum Side Length of Square Within Threshold",
    "difficulty": "Medium",
    "subtopic": "2D Search",
    "companies": ["Google", "Amazon", "Meta", "Microsoft"],
    "desc": (
        "Given an `m x n` integer matrix `mat` containing non-negative integers and an integer `threshold`, return "
        "the **maximum side length** of a contiguous square subgrid (`k x k`) whose sum of elements is less than "
        "or equal to `threshold`, or `0` if no such square exists."
    ),
    "cons": [
        "m == mat.length",
        "n == mat[i].length",
        "1 <= m, n <= 300",
        "0 <= mat[i][j] <= 10^4",
        "0 <= threshold <= 10^5",
    ],
    "hints": [
        "Build a 2D prefix sum table so the sum of any k x k square ending at (r, c) can be computed in O(1) time.",
        "Because all entries are non-negative, while scanning cells (r, c) you only ever need to test side length (best + 1): if it fits and has sum <= threshold, increment best by 1 for an O(m * n) solution.",
    ],
    "explanations": [
        "The 2x2 square of all 1s has sum 4 <= 4, while every 3x3 square has sum > 4, so the answer is 2.",
        "Every single cell is 2 > threshold 1, so no valid square exists and the answer is 0.",
        "The entire 2x2 matrix sums to 10 <= 10, giving side length 2.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "maxSideLength",
    "params": [("mat", "int[][]"), ("threshold", "int")],
    "ret": "int",
    "py": """        m, n = len(mat), len(mat[0])
        pref = [[0] * (n + 1) for _ in range(m + 1)]
        best = 0
        for r in range(1, m + 1):
            row = mat[r - 1]
            pr = pref[r]
            pr_prev = pref[r - 1]
            for c in range(1, n + 1):
                pr[c] = row[c - 1] + pr_prev[c] + pr[c - 1] - pr_prev[c - 1]
                k = best + 1
                if r >= k and c >= k:
                    sq = pr[c] - pref[r - k][c] - pr[c - k] + pref[r - k][c - k]
                    if sq <= threshold:
                        best = k
        return best""",
    "java": """        int m = mat.length, n = mat[0].length;
        int[][] pref = new int[m + 1][n + 1];
        int best = 0;
        for (int r = 1; r <= m; r++) {
            for (int c = 1; c <= n; c++) {
                pref[r][c] = mat[r - 1][c - 1] + pref[r - 1][c] + pref[r][c - 1] - pref[r - 1][c - 1];
                int k = best + 1;
                if (r >= k && c >= k) {
                    int sq = pref[r][c] - pref[r - k][c] - pref[r][c - k] + pref[r - k][c - k];
                    if (sq <= threshold) best = k;
                }
            }
        }
        return best;""",
    "visible": [
        {"mat": [[1, 1, 3, 2, 4, 3, 2], [1, 1, 3, 2, 4, 3, 2], [1, 1, 3, 2, 4, 3, 2]], "threshold": 4},
        {"mat": [[2, 2, 2, 2, 2], [2, 2, 2, 2, 2], [2, 2, 2, 2, 2]], "threshold": 1},
        {"mat": [[1, 2], [3, 4]], "threshold": 10},
    ],
    "hidden": [
        {"mat": [[0]], "threshold": 0},
        {"mat": [[5]], "threshold": 4},
        {"mat": [[5]], "threshold": 5},
        {"mat": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "threshold": 0},
        {"mat": [[1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]], "threshold": 6},
        {"mat": [[18, 70], [61, 1], [25, 85], [14, 40], [11, 96], [97, 96], [63, 45]], "threshold": 40184},
        {"mat": [[10, 10, 10], [10, 1, 1], [10, 1, 1]], "threshold": 4},
        {"mat": _rng_int_grid(6601, 20, 20, 0, 20), "threshold": 150},
        {"mat": _rng_int_grid(6602, 40, 40, 0, 50), "threshold": 2000},
    ],
})

TASKS.append({
    "slug": "67-maximum-sum-of-an-hourglass",
    "title": "Maximum Sum of an Hourglass",
    "difficulty": "Easy",
    "subtopic": "2D Search",
    "companies": ["Amazon", "Microsoft", "Bloomberg"],
    "desc": (
        "You are given an `m x n` integer matrix `grid` with `m >= 3` and `n >= 3`. An **hourglass** is a subset "
        "of 7 cells forming an `'I'`-like shape inside a `3 x 3` subgrid anchored at top-left `(r, c)`:\n\n"
        "- Top bar: `(r, c)`, `(r, c + 1)`, `(r, c + 2)`\n"
        "- Center: `(r + 1, c + 1)`\n"
        "- Bottom bar: `(r + 2, c)`, `(r + 2, c + 1)`, `(r + 2, c + 2)`\n\n"
        "Return the **maximum sum** of any hourglass in `grid`. Note that `grid` may contain negative integers."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "3 <= m, n <= 150",
        "-10^4 <= grid[i][j] <= 10^4",
    ],
    "hints": [
        "Iterate over every valid top-left anchor (r, c) with 0 <= r <= m - 3 and 0 <= c <= n - 3.",
        "Initialize the running maximum to negative infinity (not 0) since all matrix values can be negative.",
    ],
    "explanations": [
        "The hourglass anchored at (0, 0) sums 6 + 2 + 1 + 2 + 9 + 2 + 8 = 30, which is the maximum.",
        "With a 3x3 grid there is only one hourglass: 1 + 2 + 3 + 5 + 7 + 8 + 9 = 35.",
        "All entries are negative; the hourglass anchored at (0, 0) has the largest sum of -7.",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "maxHourglassSum",
    "params": [("grid", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(grid), len(grid[0])
        best = -10**18
        for r in range(m - 2):
            r0, r1, r2 = grid[r], grid[r + 1], grid[r + 2]
            for c in range(n - 2):
                s = r0[c] + r0[c + 1] + r0[c + 2] + r1[c + 1] + r2[c] + r2[c + 1] + r2[c + 2]
                if s > best:
                    best = s
        return best""",
    "java": """        int m = grid.length, n = grid[0].length;
        int best = Integer.MIN_VALUE;
        for (int r = 0; r < m - 2; r++) {
            for (int c = 0; c < n - 2; c++) {
                int s = grid[r][c] + grid[r][c + 1] + grid[r][c + 2]
                        + grid[r + 1][c + 1]
                        + grid[r + 2][c] + grid[r + 2][c + 1] + grid[r + 2][c + 2];
                if (s > best) best = s;
            }
        }
        return best;""",
    "visible": [
        {"grid": [[6, 2, 1, 3], [4, 2, 1, 5], [9, 2, 8, 7], [4, 1, 2, 9]]},
        {"grid": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        {"grid": [[-1, -1, -1], [-9, -1, -9], [-1, -1, -1]]},
    ],
    "hidden": [
        {"grid": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]},
        {"grid": [[-10, -20, -30, -1], [-5, -1, -5, -1], [-10, -20, -30, -1]]},
        {"grid": [[1, 2, 3, 4, 5], [0, 9, 0, 1, 0], [1, 2, 3, 4, 5]]},
        {"grid": [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]},
        {"grid": [[10000, 10000, 10000], [-10000, 10000, -10000], [10000, 10000, 10000]]},
        {"grid": [[-9, -9, -9, 1, 1, 1], [0, -9, 0, 4, 3, 2], [-9, -9, -9, 1, 2, 3], [0, 0, 8, 6, 6, 0], [0, 0, 0, -2, 0, 0], [0, 0, 1, 2, 4, 0]]},
        {"grid": [[5, -2, 8, 3], [9, 4, -6, 1], [-1, 7, 2, 5], [3, -8, 6, 4]]},
        {"grid": _rng_int_grid(6701, 20, 20, -50, 50)},
        {"grid": _rng_int_grid(6702, 40, 40, -1000, 1000)},
    ],
})

TASKS.append({
    "slug": "68-largest-1-bordered-square",
    "title": "Largest 1-Bordered Square",
    "difficulty": "Medium",
    "subtopic": "2D Search",
    "companies": ["Google", "Amazon", "Meta", "Salesforce"],
    "desc": (
        "Given a 2D binary matrix `grid` of `0`s and `1`s, return the **number of elements (area)** in the largest "
        "contiguous square subgrid that has all `1`s on its **border** (all four sides consist exclusively of `1`s; "
        "interior cells may be `0` or `1`). Return `0` if no such subgrid exists."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 100",
        "grid[i][j] is either 0 or 1.",
    ],
    "hints": [
        "Precompute two tables: hor[r][c] = consecutive 1s ending at (r, c) moving right, and ver[r][c] = consecutive 1s ending at (r, c) moving down.",
        "For each bottom-right corner (r, c), test candidate side lengths s from min(hor[r][c], ver[r][c]) down to best + 1; the top and left sides are valid iff hor[r - s + 1][c] >= s and ver[r][c - s + 1] >= s.",
    ],
    "explanations": [
        "The entire 3x3 grid has 1s around its border (despite the 0 in the center), so the largest area is 3 * 3 = 9.",
        "The largest 1-bordered square has side length 1, giving area 1.",
        "There are no 1s in the grid, so the largest area is 0.",
    ],
    "time": "O(m * n * min(m, n))",
    "space": "O(m * n)",
    "method": "largest1BorderedSquare",
    "params": [("grid", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(grid), len(grid[0])
        hor = [[0] * n for _ in range(m)]
        ver = [[0] * n for _ in range(m)]
        best = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1:
                    hor[r][c] = (hor[r][c - 1] if c > 0 else 0) + 1
                    ver[r][c] = (ver[r - 1][c] if r > 0 else 0) + 1
                    side = min(hor[r][c], ver[r][c])
                    while side > best:
                        if hor[r - side + 1][c] >= side and ver[r][c - side + 1] >= side:
                            best = side
                            break
                        side -= 1
        return best * best""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[][] hor = new int[m][n];
        int[][] ver = new int[m][n];
        int best = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 1) {
                    hor[r][c] = (c > 0 ? hor[r][c - 1] : 0) + 1;
                    ver[r][c] = (r > 0 ? ver[r - 1][c] : 0) + 1;
                    int side = Math.min(hor[r][c], ver[r][c]);
                    while (side > best) {
                        if (hor[r - side + 1][c] >= side && ver[r][c - side + 1] >= side) {
                            best = side;
                            break;
                        }
                        side--;
                    }
                }
            }
        }
        return best * best;""",
    "visible": [
        {"grid": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]},
        {"grid": [[1, 1, 0, 0]]},
        {"grid": [[0, 0], [0, 0]]},
    ],
    "hidden": [
        {"grid": [[1]]},
        {"grid": [[0]]},
        {"grid": [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 1], [1, 1, 1, 1]]},
        {"grid": [[1, 1, 1, 1], [1, 0, 0, 1], [1, 0, 0, 0], [1, 1, 1, 1]]},
        {"grid": [[0, 1, 1, 1], [1, 1, 0, 1], [1, 1, 1, 1], [1, 0, 1, 0]]},
        {"grid": [[1, 1], [1, 1], [1, 1]]},
        {"grid": [[1, 0, 1], [0, 1, 0], [1, 0, 1]]},
        {"grid": _rng_bin_grid(6801, 15, 15, 0.8)},
        {"grid": _rng_bin_grid(6802, 35, 35, 0.85)},
    ],
})

TASKS.append({
    "slug": "69-largest-plus-sign",
    "title": "Largest Plus Sign in Binary Grid",
    "difficulty": "Medium",
    "subtopic": "2D Search",
    "companies": ["Meta", "Amazon", "Google", "LinkedIn"],
    "desc": (
        "You are given an integer `n` representing an `n x n` binary grid initially filled with all `1`s, along with "
        "a list `mines` where each `mines[i] = [r, c]` sets cell `(r, c)` to `0`.\n\n"
        "Return the **order** `k` of the largest axis-aligned **plus sign** of `1`s contained in the grid. An "
        "order-`k` plus sign centered at `(r, c)` consists of `grid[r][c] == 1` together with four arms of length "
        "`k - 1` extending up, down, left, and right—all containing `1`s. If every cell is `0`, return `0`."
    ),
    "cons": [
        "1 <= n <= 300",
        "0 <= mines.length <= n * n",
        "mines[i].length == 2",
        "0 <= mines[i][0], mines[i][1] < n",
        "All coordinates in mines are distinct.",
    ],
    "hints": [
        "For every cell (r, c), the largest plus sign centered there has order equal to the minimum of consecutive 1s extending in each of the four directions: left, right, up, and down.",
        "Initialize an n x n array dp with n everywhere (0 at mine coordinates), then sweep each row left-to-right and right-to-left and each column top-to-bottom and bottom-to-top updating dp[r][c] = min(dp[r][c], run).",
    ],
    "explanations": [
        "With a single mine at (4, 2) in a 5x5 grid, a plus sign of order 2 fits centered at (1, 1), (1, 2), (1, 3), etc., while no order-3 plus sign fits (center (2, 2) is blocked at (4, 2)).",
        "Every cell of the 1x1 grid is a mine, so no plus sign exists (order 0).",
        "With no mines in a 3x3 grid, the center (1, 1) forms an order-2 plus sign.",
    ],
    "time": "O(n^2)",
    "space": "O(n^2)",
    "method": "orderOfLargestPlusSign",
    "params": [("n", "int"), ("mines", "int[][]")],
    "ret": "int",
    "py": """        dp = [[n] * n for _ in range(n)]
        for r, c in mines:
            dp[r][c] = 0

        for r in range(n):
            row = dp[r]
            cnt = 0
            for c in range(n):
                cnt = 0 if row[c] == 0 else cnt + 1
                if cnt < row[c]:
                    row[c] = cnt
            cnt = 0
            for c in range(n - 1, -1, -1):
                cnt = 0 if row[c] == 0 else cnt + 1
                if cnt < row[c]:
                    row[c] = cnt

        best = 0
        for c in range(n):
            cnt = 0
            for r in range(n):
                cnt = 0 if dp[r][c] == 0 else cnt + 1
                if cnt < dp[r][c]:
                    dp[r][c] = cnt
            cnt = 0
            for r in range(n - 1, -1, -1):
                cnt = 0 if dp[r][c] == 0 else cnt + 1
                if cnt < dp[r][c]:
                    dp[r][c] = cnt
                if dp[r][c] > best:
                    best = dp[r][c]
        return best""",
    "java": """        int[][] dp = new int[n][n];
        for (int[] row : dp) Arrays.fill(row, n);
        for (int[] m : mines) dp[m[0]][m[1]] = 0;

        for (int r = 0; r < n; r++) {
            int cnt = 0;
            for (int c = 0; c < n; c++) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
            }
            cnt = 0;
            for (int c = n - 1; c >= 0; c--) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
            }
        }
        int best = 0;
        for (int c = 0; c < n; c++) {
            int cnt = 0;
            for (int r = 0; r < n; r++) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
            }
            cnt = 0;
            for (int r = n - 1; r >= 0; r--) {
                cnt = (dp[r][c] == 0) ? 0 : cnt + 1;
                if (cnt < dp[r][c]) dp[r][c] = cnt;
                if (dp[r][c] > best) best = dp[r][c];
            }
        }
        return best;""",
    "visible": [
        {"n": 5, "mines": [[4, 2]]},
        {"n": 1, "mines": [[0, 0]]},
        {"n": 3, "mines": []},
    ],
    "hidden": [
        {"n": 1, "mines": []},
        {"n": 2, "mines": []},
        {"n": 2, "mines": [[0, 0], [0, 1], [1, 0], [1, 1]]},
        {"n": 5, "mines": []},
        {"n": 5, "mines": [[2, 2]]},
        {"n": 7, "mines": [[3, 3], [0, 3], [6, 3], [3, 0], [3, 6]]},
        {"n": 10, "mines": _rng_mines(6901, 10, 15)},
        {"n": 40, "mines": _rng_mines(6902, 40, 120)},
        {"n": 100, "mines": _rng_mines(6903, 100, 400)},
    ],
})

TASKS.append({
    "slug": "70-kth-smallest-number-in-multiplication-table",
    "title": "Kth Smallest Number in Multiplication Table",
    "difficulty": "Hard",
    "subtopic": "2D Search",
    "companies": ["Google", "Amazon", "Meta", "Goldman Sachs"],
    "desc": (
        "Consider an `m x n` multiplication table (1-indexed) where the cell at row `i` and column `j` holds the "
        "value `i * j` (`1 <= i <= m`, `1 <= j <= n`).\n\n"
        "Given integers `m`, `n`, and `k`, return the `k`-th smallest integer in this `m x n` multiplication table "
        "(counting duplicates with multiplicity)."
    ),
    "cons": [
        "1 <= m, n <= 3 * 10^4",
        "1 <= k <= m * n",
    ],
    "hints": [
        "Binary search the answer value x in [1, m * n] rather than building the matrix.",
        "For any candidate x, row i (which holds i, 2i, ..., n*i) contributes min(x // i, n) values <= x; sum this across all rows to check whether count(x) >= k.",
    ],
    "explanations": [
        "The 3x3 multiplication table sorted is [1, 2, 2, 3, 3, 4, 6, 6, 9]; the 5th smallest element is 3.",
        "The 2x3 multiplication table sorted is [1, 2, 2, 3, 4, 6]; the 6th smallest element is 6.",
        "The 1st smallest element in any multiplication table is always 1.",
    ],
    "time": "O(min(m, n) * log(m * n))",
    "space": "O(1)",
    "method": "findKthNumber",
    "params": [("m", "int"), ("n", "int"), ("k", "int")],
    "ret": "int",
    "py": """        if m > n:
            m, n = n, m
        lo, hi = 1, m * n
        while lo < hi:
            mid = (lo + hi) // 2
            cnt = 0
            for i in range(1, m + 1):
                q = mid // i
                if q == 0:
                    break
                cnt += n if q > n else q
            if cnt >= k:
                hi = mid
            else:
                lo = mid + 1
        return lo""",
    "java": """        if (m > n) {
            int tmp = m;
            m = n;
            n = tmp;
        }
        int lo = 1, hi = m * n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            int cnt = 0;
            for (int i = 1; i <= m; i++) {
                int q = mid / i;
                if (q == 0) break;
                cnt += Math.min(q, n);
            }
            if (cnt >= k) hi = mid;
            else lo = mid + 1;
        }
        return lo;""",
    "visible": [
        {"m": 3, "n": 3, "k": 5},
        {"m": 2, "n": 3, "k": 6},
        {"m": 4, "n": 5, "k": 1},
    ],
    "hidden": [
        {"m": 1, "n": 1, "k": 1},
        {"m": 1, "n": 100, "k": 57},
        {"m": 100, "n": 1, "k": 99},
        {"m": 3, "n": 3, "k": 4},
        {"m": 5, "n": 5, "k": 13},
        {"m": 10, "n": 12, "k": 60},
        {"m": 45, "n": 12, "k": 471},
        {"m": 1000, "n": 1000, "k": 500000},
        {"m": 30000, "n": 30000, "k": 450000000},
    ],
})

TASKS.append({
    "slug": "71-count-submatrices-with-top-left-sum-at-most-k",
    "title": "Count Submatrices with Top-Left Sum at Most K",
    "difficulty": "Medium",
    "subtopic": "2D Search",
    "companies": ["Amazon", "Google", "Microsoft", "Oracle"],
    "desc": (
        "You are given a 0-indexed `m x n` integer matrix `grid` of non-negative integers and an integer `k`.\n\n"
        "Return the number of contiguous submatrices that **contain the top-left element `(0, 0)`** (i.e., "
        "submatrices `[0..r, 0..c]` for `0 <= r < m, 0 <= c < n`) whose sum of elements is less than or equal to `k`."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 200",
        "0 <= grid[i][j] <= 10^4",
        "0 <= k <= 10^9",
    ],
    "hints": [
        "Every submatrix anchored at (0, 0) is uniquely defined by its bottom-right corner (r, c), and its sum is simply the 2D prefix sum pref[r][c].",
        "Maintain running column sums col[c] across rows and accumulate row-wise prefix sums; since all values are non-negative, break out of the inner column loop early as soon as the sum exceeds k.",
    ],
    "explanations": [
        "The 4 valid top-left submatrices end at (0,0) sum 7, (0,1) sum 13, (0,2) sum 16, and (1,0) sum 13; all others exceed 18.",
        "Six submatrices anchored at (0,0) have sums <= 20.",
        "Because grid[0][0] = 5 > k = 4, no top-left submatrix qualifies, returning 0.",
    ],
    "time": "O(m * n)",
    "space": "O(n)",
    "method": "countSubmatrices",
    "params": [("grid", "int[][]"), ("k", "int")],
    "ret": "int",
    "py": """        n = len(grid[0])
        col_sum = [0] * n
        ans = 0
        for row in grid:
            cur = 0
            for c in range(n):
                col_sum[c] += row[c]
                cur += col_sum[c]
                if cur <= k:
                    ans += 1
                else:
                    break
        return ans""",
    "java": """        int n = grid[0].length;
        long[] colSum = new long[n];
        int ans = 0;
        for (int[] row : grid) {
            long cur = 0;
            for (int c = 0; c < n; c++) {
                colSum[c] += row[c];
                cur += colSum[c];
                if (cur <= k) {
                    ans++;
                } else {
                    break;
                }
            }
        }
        return ans;""",
    "visible": [
        {"grid": [[7, 6, 3], [6, 6, 1]], "k": 18},
        {"grid": [[7, 2, 9], [1, 5, 0], [2, 6, 6]], "k": 20},
        {"grid": [[5, 1], [1, 1]], "k": 4},
    ],
    "hidden": [
        {"grid": [[0]], "k": 0},
        {"grid": [[0, 0, 0], [0, 0, 0]], "k": 0},
        {"grid": [[1, 2, 3, 4]], "k": 6},
        {"grid": [[2], [3], [4], [5]], "k": 9},
        {"grid": [[10, 0, 0], [0, 0, 0], [0, 0, 0]], "k": 10},
        {"grid": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "k": 100},
        {"grid": [[3, 4, 5], [1, 2, 1], [4, 0, 2]], "k": 12},
        {"grid": _rng_int_grid(7101, 20, 20, 0, 10), "k": 400},
        {"grid": _rng_int_grid(7102, 40, 40, 0, 50), "k": 15000},
    ],
})

# ============================================================================
# Subtopic 4: Simulation (72 - 77)
# ============================================================================

TASKS.append({
    "slug": "72-available-captures-for-rook",
    "title": "Available Captures for Rook",
    "difficulty": "Easy",
    "subtopic": "Simulation",
    "companies": ["Amazon", "Google", "Apple"],
    "desc": (
        "You are given an `m x n` character matrix `board` representing a generalized chessboard containing:\n"
        "- Exactly one white rook `'R'`\n"
        "- Zero or more white bishops `'B'`\n"
        "- Zero or more black pawns `'p'`\n"
        "- Empty squares `'.'`\n\n"
        "In a single move, the white rook moves along one of the four cardinal directions (up, down, left, or right) "
        "until it reaches the edge of the board, stops right before a friendly white bishop `'B'`, or captures the "
        "first opposing black pawn `'p'` it encounters in that direction.\n\n"
        "Return the total number of black pawns `'p'` available for the rook to capture in one move."
    ),
    "cons": [
        "m == board.length",
        "n == board[i].length",
        "1 <= m, n <= 50",
        "board[i][j] is one of 'R', 'B', 'p', or '.'.",
        "There is exactly one 'R' on the board.",
    ],
    "hints": [
        "First scan the board to locate the rook's coordinates (rr, rc).",
        "Cast four rays in directions (-1, 0), (1, 0), (0, -1), and (0, 1); stop a ray immediately upon hitting 'B', or increment the answer and stop upon hitting 'p'.",
    ],
    "explanations": [
        "The rook at (2, 2) captures the pawns to its north, west, and east (3 captures), while the bishop to its south blocks the pawn behind it.",
        "Friendly bishops surround the rook on all four sides, so 0 pawns can be captured.",
        "On a single-row board, the rook captures the nearest pawn on both its left and right (2 captures total).",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "numRookCaptures",
    "params": [("board", "char[][]")],
    "ret": "int",
    "py": """        m, n = len(board), len(board[0])
        rr = rc = 0
        for r in range(m):
            for c in range(n):
                if board[r][c] == 'R':
                    rr, rc = r, c
                    break
        captures = 0
        for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            r, c = rr + dr, rc + dc
            while 0 <= r < m and 0 <= c < n:
                ch = board[r][c]
                if ch == 'B':
                    break
                if ch == 'p':
                    captures += 1
                    break
                r += dr
                c += dc
        return captures""",
    "java": """        int m = board.length, n = board[0].length;
        int rr = 0, rc = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] == 'R') {
                    rr = r;
                    rc = c;
                }
            }
        }
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        int captures = 0;
        for (int[] d : dirs) {
            int r = rr + d[0], c = rc + d[1];
            while (r >= 0 && r < m && c >= 0 && c < n) {
                char ch = board[r][c];
                if (ch == 'B') break;
                if (ch == 'p') {
                    captures++;
                    break;
                }
                r += d[0];
                c += d[1];
            }
        }
        return captures;""",
    "visible": [
        {"board": _grid_from_rows(["..p..", ".....", "p.R.p", "..B..", "..p.."])},
        {"board": _grid_from_rows([".p.", "pBp", "BRB", "pBp", ".p."])},
        {"board": _grid_from_rows(["pp.R.pp"])},
    ],
    "hidden": [
        {"board": _grid_from_rows(["R"])},
        {"board": _grid_from_rows(["p", ".", "R", ".", "p"])},
        {"board": _grid_from_rows(["R...p", ".....", ".....", ".....", "p...."])},
        {"board": _grid_from_rows(["..p..", "..p..", "ppRpp", "..p..", "..p.."])},
        {"board": _grid_from_rows([".....", ".....", "..R..", ".....", "....."])},
        {"board": _grid_from_rows(["p.B.R", ".....", "....B", "....p"])},
        {"board": _rng_rook_board(7201, 8, 8)},
        {"board": _rng_rook_board(7202, 20, 20)},
        {"board": _rng_rook_board(7203, 40, 40)},
    ],
})

TASKS.append({
    "slug": "73-queens-that-can-attack-the-king",
    "title": "Queens That Can Attack the King",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Google", "Amazon", "Meta", "Bloomberg"],
    "desc": (
        "On an `n x n` chessboard (0-indexed), there are several black queens at positions `queens[i] = [r, c]` "
        "and a single white king at `king = [kr, kc]`.\n\n"
        "A queen can attack the king if it lies in the same row, column, or diagonal as the king AND there is no "
        "other queen directly between them blocking the line of sight.\n\n"
        "Return a 2D array of the coordinates `[r, c]` of all queens that can directly attack the king, sorted in "
        "**ascending lexicographical order** (first by `r`, then by `c`)."
    ),
    "cons": [
        "1 <= n <= 100",
        "0 <= queens.length < n * n",
        "queens[i].length == 2 and king.length == 2",
        "0 <= r, c, kr, kc < n",
        "All queen positions and the king's position are distinct.",
    ],
    "hints": [
        "Instead of checking every queen against every other queen, mark all queens on an n x n boolean grid and cast 8 directional rays outward from the king.",
        "The very first queen encountered along each of the 8 rays (if any) can attack the king; sort the collected coordinates by (r, c).",
    ],
    "explanations": [
        "Casting 8 rays from king (0, 0) hits queens at (0, 1) east, (1, 0) south, and (3, 3) south-east; (0, 4), (4, 0), and (4, 4) are blocked.",
        "All three queens at (2, 3), (1, 4), and (4, 1) have clear lines of sight to the king at (3, 3), sorted as [[1,4],[2,3],[4,1]].",
        "No queens share a row, column, or diagonal with the king at (0, 0), returning an empty list.",
    ],
    "time": "O(n + q)",
    "space": "O(n^2)",
    "method": "queensAttackTheKing",
    "params": [("n", "int"), ("queens", "int[][]"), ("king", "int[]")],
    "ret": "int[][]",
    "py": """        has_q = [[False] * n for _ in range(n)]
        for r, c in queens:
            has_q[r][c] = True
        kr, kc = king[0], king[1]
        res = []
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                r, c = kr + dr, kc + dc
                while 0 <= r < n and 0 <= c < n:
                    if has_q[r][c]:
                        res.append([r, c])
                        break
                    r += dr
                    c += dc
        res.sort()
        return res""",
    "java": """        boolean[][] hasQ = new boolean[n][n];
        for (int[] q : queens) hasQ[q[0]][q[1]] = true;
        int kr = king[0], kc = king[1];
        List<int[]> res = new ArrayList<>();
        for (int dr = -1; dr <= 1; dr++) {
            for (int dc = -1; dc <= 1; dc++) {
                if (dr == 0 && dc == 0) continue;
                int r = kr + dr, c = kc + dc;
                while (r >= 0 && r < n && c >= 0 && c < n) {
                    if (hasQ[r][c]) {
                        res.add(new int[]{r, c});
                        break;
                    }
                    r += dr;
                    c += dc;
                }
            }
        }
        res.sort((a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        return res.toArray(new int[0][]);""",
    "visible": [
        {"n": 8, "queens": [[0, 1], [1, 0], [4, 0], [0, 4], [3, 3], [2, 4], [4, 4]], "king": [0, 0]},
        {"n": 8, "queens": [[0, 0], [1, 1], [2, 2], [3, 4], [3, 5], [4, 4], [4, 5]], "king": [3, 3]},
        {"n": 5, "queens": [[1, 2], [2, 1], [3, 4]], "king": [0, 0]},
    ],
    "hidden": [
        {"n": 1, "queens": [], "king": [0, 0]},
        {"n": 8, "queens": [], "king": [4, 4]},
        {"n": 3, "queens": [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]], "king": [1, 1]},
        {"n": 8, "queens": [[0, 3], [1, 3], [2, 3], [5, 3], [6, 3], [7, 3]], "king": [3, 3]},
        {"n": 8, "queens": [[5, 6], [7, 7], [2, 1], [0, 7], [1, 6], [5, 1], [3, 7], [0, 3], [4, 0], [1, 2], [6, 3], [5, 0], [0, 4], [2, 2], [1, 1], [6, 4], [5, 4], [0, 0], [2, 6], [4, 5], [5, 2], [1, 4], [7, 5], [2, 3], [0, 5], [4, 2], [1, 0], [2, 7], [0, 1], [4, 6], [6, 1], [0, 6], [4, 3], [1, 7]], "king": [3, 4]},
        {"n": 10, "queens": [[0, 0], [9, 9], [0, 9], [9, 0], [0, 5], [9, 5], [5, 0], [5, 9]], "king": [5, 5]},
        _rng_queens_case(7301, 15, 25),
        _rng_queens_case(7302, 40, 100),
        _rng_queens_case(7303, 100, 300),
    ],
})
# Fix explanation #2 for problem 73 to match visible test #2 accurately!
TASKS[-1]["explanations"][1] = (
    "From king (3, 3), the attacking queens are (2, 2) north-west, (3, 4) east, and (4, 4) south-east; "
    "(0, 0), (1, 1), and (3, 5) are blocked, giving [[2,2],[3,4],[4,4]]."
)

TASKS.append({
    "slug": "74-valid-tic-tac-toe-state",
    "title": "Valid Tic-Tac-Toe Board State",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Microsoft", "Amazon", "Meta", "Apple"],
    "desc": (
        "Given a `3 x 3` Tic-Tac-Toe board represented as a string array `board` of length `3`, where each string "
        "has length `3` and contains only `'X'`, `'O'`, or space `' '`, return `true` if and only if it is possible "
        "to reach this board state during the course of a valid Tic-Tac-Toe game.\n\n"
        "The rules of Tic-Tac-Toe are:\n"
        "1. Players take turns placing marks into empty squares (`' '`), with `'X'` always playing first.\n"
        "2. The game ends immediately as soon as any row, column, or main/anti-diagonal contains three identical "
        "non-empty marks (or all 9 squares are filled).\n"
        "3. No more moves can be made after the game ends."
    ),
    "cons": [
        "board.length == 3",
        "board[i].length == 3",
        "board[i][j] is either 'X', 'O', or ' '.",
    ],
    "hints": [
        "Because 'X' always moves first and players alternate, count(X) must equal count(O) or count(O) + 1.",
        "Check whether 'X' has a winning line and whether 'O' has a winning line: both cannot win simultaneously, if 'X' wins then count(X) must equal count(O) + 1, and if 'O' wins then count(X) must equal count(O).",
    ],
    "explanations": [
        "'O' cannot play before 'X' makes the first move, so count(X) = 0 and count(O) = 1 is invalid.",
        "'X' has 3 marks while 'O' has only 1 mark, violating alternating turns.",
        "With 4 'X's, 4 'O's, and no winner yet, this mid-game board state is reachable.",
    ],
    "time": "O(1)",
    "space": "O(1)",
    "method": "validTicTacToe",
    "params": [("board", "String[]")],
    "ret": "boolean",
    "py": """        x_cnt = sum(row.count('X') for row in board)
        o_cnt = sum(row.count('O') for row in board)
        if x_cnt != o_cnt and x_cnt != o_cnt + 1:
            return False

        def wins(ch: str) -> bool:
            for i in range(3):
                if board[i][0] == board[i][1] == board[i][2] == ch:
                    return True
                if board[0][i] == board[1][i] == board[2][i] == ch:
                    return True
            if board[0][0] == board[1][1] == board[2][2] == ch:
                return True
            if board[0][2] == board[1][1] == board[2][0] == ch:
                return True
            return False

        x_win = wins('X')
        o_win = wins('O')
        if x_win and o_win:
            return False
        if x_win and x_cnt != o_cnt + 1:
            return False
        if o_win and x_cnt != o_cnt:
            return False
        return True""",
    "java": """        int xCnt = 0, oCnt = 0;
        for (int r = 0; r < 3; r++) {
            for (int c = 0; c < 3; c++) {
                char ch = board[r].charAt(c);
                if (ch == 'X') xCnt++;
                else if (ch == 'O') oCnt++;
            }
        }
        if (xCnt != oCnt && xCnt != oCnt + 1) return false;
        boolean xWin = wins(board, 'X');
        boolean oWin = wins(board, 'O');
        if (xWin && oWin) return false;
        if (xWin && xCnt != oCnt + 1) return false;
        if (oWin && xCnt != oCnt) return false;
        return true;""",
    "java_helpers": """    private boolean wins(String[] b, char ch) {
        for (int i = 0; i < 3; i++) {
            if (b[i].charAt(0) == ch && b[i].charAt(1) == ch && b[i].charAt(2) == ch) return true;
            if (b[0].charAt(i) == ch && b[1].charAt(i) == ch && b[2].charAt(i) == ch) return true;
        }
        if (b[0].charAt(0) == ch && b[1].charAt(1) == ch && b[2].charAt(2) == ch) return true;
        if (b[0].charAt(2) == ch && b[1].charAt(1) == ch && b[2].charAt(0) == ch) return true;
        return false;
    }""",
    "visible": [
        {"board": ["O  ", "   ", "   "]},
        {"board": ["XOX", " X ", "   "]},
        {"board": ["XOX", "O O", "XOX"]},
    ],
    "hidden": [
        {"board": ["   ", "   ", "   "]},
        {"board": ["XXX", "   ", "OOO"]},
        {"board": ["XXX", "OO ", "   "]},
        {"board": ["XXX", "OO ", "O  "]},
        {"board": ["OOO", "XX ", "X  "]},
        {"board": ["OOO", "XX ", "XX "]},
        {"board": ["XXX", "XOO", "OO "]},
        {"board": ["XOX", "OXO", "XOX"]},
        {"board": ["OXX", "XOX", "OXO"]},
    ],
})

TASKS.append({
    "slug": "75-laser-beam-reflection-in-mirror-grid",
    "title": "Laser Beam Reflection in Mirror Grid",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Google", "Amazon", "Apple", "Uber"],
    "desc": (
        "You are given an `m x n` character matrix `grid` representing a room containing mirrors:\n"
        "- `'.'` is an empty cell where a laser beam continues straight.\n"
        "- `'/'` is a diagonal mirror reflecting `Right -> Up`, `Up -> Right`, `Left -> Down`, `Down -> Left`.\n"
        "- `'\\\\'` is a diagonal mirror reflecting `Right -> Down`, `Down -> Right`, `Left -> Up`, `Up -> Left`.\n\n"
        "A laser beam enters cell `(0, 0)` moving **Right**. Whenever the beam enters a cell, that cell becomes "
        "illuminated, the beam adjusts its direction according to the cell's character, and then moves one step in "
        "its new direction. The beam terminates when it exits the grid or enters a `(row, col, direction)` state "
        "it has previously visited.\n\n"
        "Return the total number of **distinct cells** illuminated by the laser beam."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 100",
        "grid[i][j] is one of '.', '/', or '\\\\'.",
    ],
    "hints": [
        "Encode directions as 0=Right, 1=Down, 2=Left, 3=Up: then '/' maps d to 3 - d and '\\\\' maps d to d ^ 1.",
        "Track visited (r, c, dir) states using a 4-bit bitmask per cell to detect cycles in O(1), and count each cell the first time its mask transitions from 0 to non-zero.",
    ],
    "explanations": [
        "The beam moves right across (0,0), (0,1), reflects down at (0,2)='\\\\', moves through (1,2), reflects left at (2,2)='/', and exits past (2,0) after lighting 7 cells.",
        "The beam hits '/' at (0,0), reflects upward immediately out of bounds, illuminating only 1 cell.",
        "Four mirrors at the corners bounce the beam around a closed 2x2 cycle, illuminating all 4 distinct cells before repeating a state.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "illuminatedCells",
    "params": [("grid", "char[][]")],
    "ret": "int",
    "py": """        m, n = len(grid), len(grid[0])
        dr = (0, 1, 0, -1)
        dc = (1, 0, -1, 0)
        seen = [[0] * n for _ in range(m)]
        r = c = d = 0
        lit = 0
        while 0 <= r < m and 0 <= c < n:
            bit = 1 << d
            if seen[r][c] & bit:
                break
            if seen[r][c] == 0:
                lit += 1
            seen[r][c] |= bit
            ch = grid[r][c]
            if ch == '/':
                d = 3 - d
            elif ch == '\\\\':
                d ^= 1
            r += dr[d]
            c += dc[d]
        return lit""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[] dr = {0, 1, 0, -1};
        int[] dc = {1, 0, -1, 0};
        int[][] seen = new int[m][n];
        int r = 0, c = 0, d = 0, lit = 0;
        while (r >= 0 && r < m && c >= 0 && c < n) {
            int bit = 1 << d;
            if ((seen[r][c] & bit) != 0) break;
            if (seen[r][c] == 0) lit++;
            seen[r][c] |= bit;
            char ch = grid[r][c];
            if (ch == '/') d = 3 - d;
            else if (ch == '\\\\') d ^= 1;
            r += dr[d];
            c += dc[d];
        }
        return lit;""",
    "visible": [
        {"grid": _grid_from_rows(["..\\", "...", "../"])},
        {"grid": _grid_from_rows(["/.", ".."])},
        {"grid": _grid_from_rows([".\\", "\\/"])},
    ],
    "hidden": [
        {"grid": _grid_from_rows(["."])},
        {"grid": _grid_from_rows(["\\"])},
        {"grid": _grid_from_rows(["....."])},
        {"grid": _grid_from_rows(["\\.", "./"])},
        {"grid": _grid_from_rows([".\\.\\", "\\./.", "././"])},
        {"grid": _grid_from_rows(["..\\..", ".....", "/.\\..", ".....", "\\.../"] )},
        {"grid": _grid_from_rows(["...\\", "\\..\\", "/../", "\\../"])},
        {"grid": _rng_mirror_grid(7501, 15, 15)},
        {"grid": _rng_mirror_grid(7502, 40, 40)},
    ],
})
# Verify visible #3 for 75: grid = [".\", "\/"]
# (0,0)='.' R->(0,1)='\' D->(1,1)='/' L->(1,0)='\' U->(0,0)='.' U->(-1,0) OOB! Wait, that exits instead of cycling, still lights all 4 cells!
# Let's make visible #3 an actual closed cycle: 2x3: [".\.", "\./"] -> wait: (0,0)='.' R->(0,1)='\' D->(1,1)='.' D->OOB.
# For an actual closed cycle starting at (0,0) moving R:
# Row 0: . / . \   (no, (0,1)='/' goes UP OOB).
# To enter a loop from (0,0) moving R:
# (0,0)='.' R -> (0,1)='.' R -> (0,2)='\' D -> (1,2)='/' L -> (1,1)='\' U -> (0,1)='/' R -> (0,2)='\' ... YES!
# Wait: at (0,1)='/' when coming from Left (0,0), it goes UP!
# Instead:
# (0,0)='.' R -> (0,1)='\' D -> (1,1)='\' R -> (1,2)='/' U -> (0,2)='.'? No, put '/' at (0,1)?
# Wait: a beam entering at (0,0) can NEVER cycle back into (0,0) moving R because nothing is left of (0,0), UNLESS (0,0) is visited again from another direction? Even then, if it enters a cell from Down and turns Right into a loop, it DOES cycle!
# Check 3x3:
# Row 0: . . \    (0,0) R->(0,1) R->(0,2)='\' D->(1,2)
# Row 1: . / \    (1,2)='\' R->OOB. Wait: make (1,2)='.', (2,2)='/' L->(2,1)='\' U->(1,1)='/' R->(1,2)='\' D->(2,2)!
# Let's trace 3x3:
# [".", ".", "\\"]
# [".", "/", "\\"]
# [".", "\\", "/"]
# (0,0) R -> (0,1) R -> (0,2)='\' D -> (1,2)='\' R -> OOB! Wait: (1,2) is '\' so coming from Up (d=1, Down) it maps d^1 = 0 (Right)!
# We want (1,2) to let Down pass straight ('.')! Then (2,2)='/' L -> (2,1)='\' U -> (1,1)='/' R -> (1,2)='.' R -> OOB!
# Ah! To close the loop, we need 4 mirrors in a rectangle AND an entry into one of them — wait: every mirror is a bijection on directions, so a beam is reversible! A beam entering from outside the boundary can NEVER enter a cycle inside a finite grid of reversible mirrors (each mirror is 1-to-1, so every cell-direction has in-degree 1 and out-degree 1, meaning paths starting on the boundary MUST exit on the boundary)!
# WHOA! Good catch! Because '/' and '\' are bijections on the 4 directions, by reversibility a beam entering from outside NEVER loops! Every path exits!
# Let's update the description and visible #3 explanation of problem 75 so we don't falsely claim a cycle happens in visible #3!
TASKS[-1]["visible"][2] = {"grid": _grid_from_rows(["\\..", "\\/.", "..."])}
TASKS[-1]["explanations"][2] = (
    "The beam reflects down at (0,0)='\\\\', right at (1,0)='\\\\', up at (1,1)='/', and exits through (0,1), "
    "illuminating 4 distinct cells."
)

TASKS.append({
    "slug": "76-projection-area-of-3d-shapes",
    "title": "Projection Area of 3D Shapes",
    "difficulty": "Easy",
    "subtopic": "Simulation",
    "companies": ["Google", "Amazon", "Adobe"],
    "desc": (
        "You are given an `n x n` integer matrix `grid` where we place stacks of `1 x 1 x 1` cubes aligned with "
        "the `x`, `y`, and `z` axes. Specifically, `grid[i][j]` represents a vertical tower of `grid[i][j]` cubes "
        "placed on top of grid cell `(i, j)`.\n\n"
        "We view the **projection** (shadow) of these cubes onto the `xy`, `yz`, and `zx` planes:\n"
        "- The `xy` (top) projection area equals the number of cells `(i, j)` with `grid[i][j] > 0`.\n"
        "- The `yz` (front) projection area equals the sum of the maximum value in each row.\n"
        "- The `zx` (side) projection area equals the sum of the maximum value in each column.\n\n"
        "Return the total area of all three projections combined."
    ),
    "cons": [
        "n == grid.length == grid[i].length",
        "1 <= n <= 50",
        "0 <= grid[i][j] <= 50",
    ],
    "hints": [
        "In a single double loop over i and j, count non-zero cells while tracking rowMax = max_j grid[i][j] and colMax = max_j grid[j][i].",
        "Add rowMax and colMax to the total area at the end of each outer iteration i, using O(1) extra space.",
    ],
    "explanations": [
        "Top area = 4 (all 4 cells > 0), front area = 2 + 4 = 6, side area = 3 + 4 = 7; total = 4 + 6 + 7 = 17.",
        "A single tower of height 2 has top area 1, front area 2, and side area 2, totaling 5.",
        "Top area = 2 (two non-zero cells), front area = 1 + 2 = 3, side area = 1 + 2 = 3; total = 8.",
    ],
    "time": "O(n^2)",
    "space": "O(1)",
    "method": "projectionArea",
    "params": [("grid", "int[][]")],
    "ret": "int",
    "py": """        n = len(grid)
        total = 0
        for i in range(n):
            row_max = 0
            col_max = 0
            for j in range(n):
                if grid[i][j] > 0:
                    total += 1
                if grid[i][j] > row_max:
                    row_max = grid[i][j]
                if grid[j][i] > col_max:
                    col_max = grid[j][i]
            total += row_max + col_max
        return total""",
    "java": """        int n = grid.length;
        int total = 0;
        for (int i = 0; i < n; i++) {
            int rowMax = 0, colMax = 0;
            for (int j = 0; j < n; j++) {
                if (grid[i][j] > 0) total++;
                if (grid[i][j] > rowMax) rowMax = grid[i][j];
                if (grid[j][i] > colMax) colMax = grid[j][i];
            }
            total += rowMax + colMax;
        }
        return total;""",
    "visible": [
        {"grid": [[1, 2], [3, 4]]},
        {"grid": [[2]]},
        {"grid": [[1, 0], [0, 2]]},
    ],
    "hidden": [
        {"grid": [[0]]},
        {"grid": [[0, 0], [0, 0]]},
        {"grid": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]},
        {"grid": [[2, 2, 2], [2, 1, 2], [2, 2, 2]]},
        {"grid": [[50, 0, 0], [0, 0, 0], [0, 0, 50]]},
        {"grid": [[0, 3, 1], [2, 0, 4], [5, 1, 0]]},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]},
        {"grid": _rng_int_grid(7601, 15, 15, 0, 50)},
        {"grid": _rng_int_grid(7602, 40, 40, 0, 50)},
    ],
})

TASKS.append({
    "slug": "77-langtons-ant-grid-simulation",
    "title": "Langton's Ant Grid Simulation",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Google", "Meta", "Microsoft", "Atlassian"],
    "desc": (
        "You are given an `m x n` binary matrix `grid` (`0` = white, `1` = black), a starting cell "
        "`(startRow, startCol)`, and a non-negative integer `steps`.\n\n"
        "An ant starts at `(startRow, startCol)` facing **North (Up)**. In each step (up to `steps` steps):\n"
        "1. If the ant's current cell is `0` (white), turn **90 degrees clockwise** and flip the cell to `1`.\n"
        "2. If the ant's current cell is `1` (black), turn **90 degrees counter-clockwise** and flip the cell to `0`.\n"
        "3. Move one cell forward in the ant's new facing direction.\n"
        "4. If moving forward takes the ant outside the `m x n` grid, stop immediately.\n\n"
        "Return the final `m x n` binary grid after all steps complete (or after the ant exits the grid)."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 100",
        "grid[i][j] is either 0 or 1.",
        "0 <= startRow < m, 0 <= startCol < n",
        "0 <= steps <= 10^5",
    ],
    "hints": [
        "Encode the four clockwise directions as 0=North(-1,0), 1=East(0,1), 2=South(1,0), 3=West(0,-1); then clockwise turn is (d + 1) % 4 and counter-clockwise turn is (d + 3) % 4.",
        "Work on a copy of grid and break out of the step loop immediately whenever the next coordinate (r, c) goes out of bounds.",
    ],
    "explanations": [
        "Starting at center (1,1) facing North on an all-white 3x3 grid, the ant flips (1,1), turns East to (1,2), flips it, turns South to (2,2), flips it, turns West to (2,1), flips it, and returns to (1,1).",
        "On step 1 at (0,0)=0, the ant flips (0,0) to 1 and moves East to (0,1); on step 2 at (0,1)=1, it flips (0,1) to 0, turns North, and exits the grid early.",
        "With steps = 0, no moves occur and the original grid is returned unchanged.",
    ],
    "time": "O(m * n + steps)",
    "space": "O(m * n)",
    "method": "simulateLangtonsAnt",
    "params": [("grid", "int[][]"), ("startRow", "int"), ("startCol", "int"), ("steps", "int")],
    "ret": "int[][]",
    "py": """        m, n = len(grid), len(grid[0])
        res = [row[:] for row in grid]
        dr = (-1, 0, 1, 0)
        dc = (0, 1, 0, -1)
        r, c, d = startRow, startCol, 0
        for _ in range(steps):
            if res[r][c] == 0:
                d = (d + 1) % 4
                res[r][c] = 1
            else:
                d = (d + 3) % 4
                res[r][c] = 0
            r += dr[d]
            c += dc[d]
            if r < 0 or r >= m or c < 0 or c >= n:
                break
        return res""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        for (int i = 0; i < m; i++) res[i] = grid[i].clone();
        int[] dr = {-1, 0, 1, 0};
        int[] dc = {0, 1, 0, -1};
        int r = startRow, c = startCol, d = 0;
        for (int s = 0; s < steps; s++) {
            if (res[r][c] == 0) {
                d = (d + 1) % 4;
                res[r][c] = 1;
            } else {
                d = (d + 3) % 4;
                res[r][c] = 0;
            }
            r += dr[d];
            c += dc[d];
            if (r < 0 || r >= m || c < 0 || c >= n) break;
        }
        return res;""",
    "visible": [
        {"grid": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "startRow": 1, "startCol": 1, "steps": 4},
        {"grid": [[0, 1], [0, 0]], "startRow": 0, "startCol": 0, "steps": 10},
        {"grid": [[1, 0], [0, 1]], "startRow": 1, "startCol": 0, "steps": 0},
    ],
    "hidden": [
        {"grid": [[0]], "startRow": 0, "startCol": 0, "steps": 5},
        {"grid": [[1]], "startRow": 0, "startCol": 0, "steps": 1},
        {"grid": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], "startRow": 2, "startCol": 2, "steps": 25},
        {"grid": [[1, 1, 1], [1, 1, 1], [1, 1, 1]], "startRow": 1, "startCol": 1, "steps": 8},
        {"grid": [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]], "startRow": 2, "startCol": 1, "steps": 15},
        {"grid": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "startRow": 1, "startCol": 1, "steps": 500},
        {"grid": _rng_bin_grid(7701, 12, 12, 0.3), "startRow": 6, "startCol": 6, "steps": 200},
        {"grid": [[0] * 25 for _ in range(25)], "startRow": 12, "startCol": 12, "steps": 1000},
        {"grid": [[0] * 35 for _ in range(35)], "startRow": 17, "startCol": 17, "steps": 5000},
    ],
})

# ============================================================================
# Subtopic 5: Dynamic Grids (78 - 83)
# ============================================================================

TASKS.append({
    "slug": "78-grid-illumination-queries",
    "title": "Grid Illumination Queries",
    "difficulty": "Hard",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Amazon", "Meta", "Uber"],
    "desc": (
        "There is a 2D `n x n` grid where every cell is initially turned off. You are given a 2D array `lamps`, "
        "where `lamps[i] = [row, col]` turns on a lamp at `(row, col)` (note: `lamps` may contain duplicate "
        "coordinates referring to the same lamp). Each active lamp illuminates its own cell plus every cell in "
        "the same **row**, same **column**, and both **diagonals**.\n\n"
        "You are also given `queries`, where `queries[j] = [qr, qc]`. Process each query sequentially:\n"
        "1. Record `1` if `(qr, qc)` is currently illuminated by at least one active lamp, or `0` otherwise.\n"
        "2. Immediately after answering, turn off every active lamp located at `(qr, qc)` or any of its 8 adjacent "
        "neighbors (the `3 x 3` neighborhood centered at `(qr, qc)`).\n\n"
        "Return an integer array `ans` of length `queries.length` containing the result for each query."
    ),
    "cons": [
        "1 <= n <= 10^9",
        "0 <= lamps.length <= 2 * 10^4",
        "0 <= queries.length <= 2 * 10^4",
        "lamps[i].length == 2 and queries[j].length == 2",
        "0 <= row, col < n",
    ],
    "hints": [
        "Store active lamp coordinates in a hash set (deduplicating input lamps) and maintain four hash maps counting active lamps on each row r, column c, main diagonal (r - c), and anti-diagonal (r + c).",
        "A query cell (qr, qc) is lit iff any of its four line counters is > 0; then inspect all 9 cells in its 3x3 neighborhood and remove any active lamp while decrementing all four counters.",
    ],
    "explanations": [
        "Query (1,1) is lit diagonally by both (0,0) and (4,4), returning 1, and turns off the lamp at (0,0); query (1,0) is no longer lit by (4,4), returning 0.",
        "Query (1,1) is lit by (0,0) and (0,4), turning off (0,0); query (1,1) again is still lit diagonally by (0,4)? No—(1,1) is not on (0,4)'s row/col/diagonals, so wait: (0,4) has r+c=4 while (1,1) has r+c=2; thus second query (1,1) returns 0.",
        "Duplicate lamp [0,0] is turned on only once, so after query (1,1) turns it off, query (0,0) sees 0 active lamps and returns 0.",
    ],
    "time": "O(L + Q)",
    "space": "O(L)",
    "method": "gridIllumination",
    "params": [("n", "int"), ("lamps", "int[][]"), ("queries", "int[][]")],
    "ret": "int[]",
    "py": """        active = set()
        rows = defaultdict(int)
        cols = defaultdict(int)
        d1 = defaultdict(int)
        d2 = defaultdict(int)
        for r, c in lamps:
            if (r, c) not in active:
                active.add((r, c))
                rows[r] += 1
                cols[c] += 1
                d1[r - c] += 1
                d2[r + c] += 1

        ans = []
        for qr, qc in queries:
            if rows[qr] > 0 or cols[qc] > 0 or d1[qr - qc] > 0 or d2[qr + qc] > 0:
                ans.append(1)
            else:
                ans.append(0)
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = qr + dr, qc + dc
                    if (nr, nc) in active:
                        active.remove((nr, nc))
                        rows[nr] -= 1
                        cols[nc] -= 1
                        d1[nr - nc] -= 1
                        d2[nr + nc] -= 1
        return ans""",
    "java": """        Set<Long> active = new HashSet<>();
        Map<Integer, Integer> rows = new HashMap<>();
        Map<Integer, Integer> cols = new HashMap<>();
        Map<Integer, Integer> d1 = new HashMap<>();
        Map<Integer, Integer> d2 = new HashMap<>();
        for (int[] lamp : lamps) {
            int r = lamp[0], c = lamp[1];
            long key = (((long) r) << 32) | (c & 0xffffffffL);
            if (active.add(key)) {
                rows.merge(r, 1, Integer::sum);
                cols.merge(c, 1, Integer::sum);
                d1.merge(r - c, 1, Integer::sum);
                d2.merge(r + c, 1, Integer::sum);
            }
        }
        int[] ans = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int qr = queries[i][0], qc = queries[i][1];
            if (rows.getOrDefault(qr, 0) > 0
                    || cols.getOrDefault(qc, 0) > 0
                    || d1.getOrDefault(qr - qc, 0) > 0
                    || d2.getOrDefault(qr + qc, 0) > 0) {
                ans[i] = 1;
            }
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    int nr = qr + dr, nc = qc + dc;
                    if (nr >= 0 && nr < n && nc >= 0 && nc < n) {
                        long key = (((long) nr) << 32) | (nc & 0xffffffffL);
                        if (active.remove(key)) {
                            rows.merge(nr, -1, Integer::sum);
                            cols.merge(nc, -1, Integer::sum);
                            d1.merge(nr - nc, -1, Integer::sum);
                            d2.merge(nr + nc, -1, Integer::sum);
                        }
                    }
                }
            }
        }
        return ans;""",
    "visible": [
        {"n": 5, "lamps": [[0, 0], [4, 4]], "queries": [[1, 1], [1, 0]]},
        {"n": 5, "lamps": [[0, 0], [0, 4]], "queries": [[0, 4], [0, 1], [1, 4]]},
        {"n": 5, "lamps": [[0, 0], [0, 0]], "queries": [[1, 1], [0, 0]]},
    ],
    "hidden": [
        {"n": 1, "lamps": [[0, 0]], "queries": [[0, 0], [0, 0]]},
        {"n": 5, "lamps": [], "queries": [[0, 0], [2, 2], [4, 4]]},
        {"n": 5, "lamps": [[0, 0], [4, 4]], "queries": [[1, 1], [1, 1]]},
        {"n": 10, "lamps": [[2, 5], [7, 0], [9, 9], [2, 5]], "queries": [[5, 2], [2, 2], [7, 7], [0, 0]]},
        {"n": 1000000000, "lamps": [[0, 0], [999999999, 999999999], [0, 999999999]], "queries": [[500000000, 500000000], [1, 1], [500000000, 500000000], [999999999, 0]]},
        {"n": 6, "lamps": [[1, 1], [1, 2], [2, 1], [2, 2]], "queries": [[1, 1], [2, 2], [0, 0]]},
        _rng_illumination(7801, 20, 30, 40),
        _rng_illumination(7802, 500, 200, 250),
        _rng_illumination(7803, 1000000000, 1000, 1000),
    ],
})
# Update explanation #2 for problem 78 to cleanly match visible test #2!
TASKS[-1]["explanations"][1] = (
    "Query (0,4) is lit (1) and turns off lamp (0,4); query (0,1) is still lit by row-0 lamp (0,0) (1) and turns "
    "off (0,0); query (1,4) has no remaining active lamps, returning 0."
)

TASKS.append({
    "slug": "79-range-sum-query-2d-mutable",
    "title": "Range Sum Query 2D - Mutable",
    "difficulty": "Hard",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Meta", "Amazon", "Bloomberg"],
    "desc": (
        "Design a data structure `NumMatrix2D` over an `m x n` integer matrix that efficiently handles point updates "
        "and rectangular range sum queries:\n\n"
        "- `NumMatrix2D(int[][] matrix)` initializes the object with the `m x n` integer matrix `matrix`.\n"
        "- `void update(int row, int col, int val)` updates the value at `matrix[row][col]` to `val`.\n"
        "- `int sumRegion(int row1, int col1, int row2, int col2)` returns the sum of elements inside the "
        "axis-aligned rectangle defined by upper-left corner `(row1, col1)` and lower-right corner `(row2, col2)` "
        "inclusive."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 200",
        "-1000 <= matrix[i][j], val <= 1000",
        "0 <= row1 <= row2 < m, 0 <= col1 <= col2 < n",
        "At most 10^4 calls will be made to update and sumRegion.",
    ],
    "hints": [
        "Store a 2D Fenwick tree (Binary Indexed Tree) of size (m + 1) x (n + 1) together with the current matrix values so each update(row, col, val) applies delta = val - current[row][col].",
        "Answer sumRegion(r1, c1, r2, c2) via inclusion-exclusion over four O(log m * log n) 2D prefix queries.",
    ],
    "explanations": [
        "Initially the subgrid [2..4, 1..3] sums to 8; after updating (3, 2) from 1 to 2, the same subgrid sums to 10? Wait: check exact matrix values.",
        "Updating (0, 0) from 1 to 5 changes the 2x2 total sum from 10 to 14.",
        "On a 1x1 matrix, updating the sole cell from -3 to 7 changes its region sum from -3 to 7.",
    ],
    "time": "O(log m * log n) per operation",
    "space": "O(m * n)",
    "kind": "design",
    "className": "NumMatrix2D",
    "constructor": [("matrix", "int[][]")],
    "methods": [
        ("update", [("row", "int"), ("col", "int"), ("val", "int")], "void"),
        ("sumRegion", [("row1", "int"), ("col1", "int"), ("row2", "int"), ("col2", "int")], "int"),
    ],
    "py_class": """class NumMatrix2D:
    def __init__(self, matrix: List[List[int]]):
        self.m = len(matrix)
        self.n = len(matrix[0])
        self.vals = [[0] * self.n for _ in range(self.m)]
        self.bit = [[0] * (self.n + 1) for _ in range(self.m + 1)]
        for r in range(self.m):
            for c in range(self.n):
                self.update(r, c, matrix[r][c])

    def update(self, row: int, col: int, val: int) -> None:
        delta = val - self.vals[row][col]
        self.vals[row][col] = val
        i = row + 1
        while i <= self.m:
            j = col + 1
            row_bit = self.bit[i]
            while j <= self.n:
                row_bit[j] += delta
                j += j & -j
            i += i & -i

    def _prefix(self, r: int, c: int) -> int:
        total = 0
        i = r
        while i > 0:
            j = c
            row_bit = self.bit[i]
            while j > 0:
                total += row_bit[j]
                j -= j & -j
            i -= i & -i
        return total

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self._prefix(row2 + 1, col2 + 1)
            - self._prefix(row1, col2 + 1)
            - self._prefix(row2 + 1, col1)
            + self._prefix(row1, col1)
        )""",
    "java_class": """class NumMatrix2D {
    private final int m, n;
    private final int[][] vals;
    private final int[][] bit;

    public NumMatrix2D(int[][] matrix) {
        this.m = matrix.length;
        this.n = matrix[0].length;
        this.vals = new int[m][n];
        this.bit = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                update(r, c, matrix[r][c]);
            }
        }
    }

    public void update(int row, int col, int val) {
        int delta = val - vals[row][col];
        vals[row][col] = val;
        for (int i = row + 1; i <= m; i += i & -i) {
            for (int j = col + 1; j <= n; j += j & -j) {
                bit[i][j] += delta;
            }
        }
    }

    private int prefix(int r, int c) {
        int total = 0;
        for (int i = r; i > 0; i -= i & -i) {
            for (int j = c; j > 0; j -= j & -j) {
                total += bit[i][j];
            }
        }
        return total;
    }

    public int sumRegion(int row1, int col1, int row2, int col2) {
        return prefix(row2 + 1, col2 + 1)
                - prefix(row1, col2 + 1)
                - prefix(row2 + 1, col1)
                + prefix(row1, col1);
    }
}""",
    "visible": [
        {
            "ops": ["NumMatrix2D", "sumRegion", "update", "sumRegion"],
            "args": [
                [[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]],
                [2, 1, 4, 3],
                [3, 2, 2],
                [2, 1, 4, 3],
            ],
        },
        {
            "ops": ["NumMatrix2D", "sumRegion", "update", "sumRegion"],
            "args": [[[[1, 2], [3, 4]]], [0, 0, 1, 1], [0, 0, 5], [0, 0, 1, 1]],
        },
        {
            "ops": ["NumMatrix2D", "sumRegion", "update", "sumRegion"],
            "args": [[[[-3]]], [0, 0, 0, 0], [0, 0, 7], [0, 0, 0, 0]],
        },
    ],
    "hidden": [
        {
            "ops": ["NumMatrix2D", "update", "sumRegion", "update", "sumRegion"],
            "args": [[[[0, 0, 0]]], [0, 1, 5], [0, 0, 0, 2], [0, 1, -4], [0, 1, 0, 1]],
        },
        {
            "ops": ["NumMatrix2D", "sumRegion", "update", "sumRegion"],
            "args": [[[[2], [-3], [4], [-5]]], [0, 0, 3, 0], [1, 0, 10], [0, 0, 2, 0]],
        },
        {
            "ops": ["NumMatrix2D", "update", "update", "sumRegion", "sumRegion"],
            "args": [[[[1, 1, 1], [1, 1, 1], [1, 1, 1]]], [0, 0, 10], [2, 2, -5], [0, 0, 2, 2], [1, 1, 2, 2]],
        },
        {
            "ops": ["NumMatrix2D", "sumRegion", "update", "update", "sumRegion"],
            "args": [[[[10, -2, 5], [3, 4, -1]]], [0, 1, 1, 2], [0, 1, 8], [1, 2, 9], [0, 0, 1, 2]],
        },
        {
            "ops": ["NumMatrix2D", "update", "update", "update", "sumRegion"],
            "args": [[[[5, 5], [5, 5]]], [0, 0, 0], [0, 0, 10], [0, 0, -3], [0, 0, 0, 1]],
        },
        _rng_num_matrix_2d_ops(7901, 5, 5, 25),
        _rng_num_matrix_2d_ops(7902, 10, 12, 60),
        _rng_num_matrix_2d_ops(7903, 20, 20, 150),
        _rng_num_matrix_2d_ops(7904, 30, 30, 400),
    ],
})
# Clean up explanation #1 for problem 79!
TASKS[-1]["explanations"][0] = (
    "Initially subgrid [2..4, 1..3] sums to 8; updating cell (3, 2) from 0 to 2 increases that region sum to 10."
)

TASKS.append({
    "slug": "80-cells-with-odd-values-in-a-matrix",
    "title": "Cells with Odd Values in a Matrix",
    "difficulty": "Easy",
    "subtopic": "Dynamic Grids",
    "companies": ["Amazon", "Google", "Apple"],
    "desc": (
        "There is an `m x n` matrix initialized to all `0`s. You are given a 2D integer array `indices` where each "
        "`indices[i] = [ri, ci]` represents an operation that:\n"
        "1. Increments every cell in row `ri` by `1`.\n"
        "2. Increments every cell in column `ci` by `1`.\n\n"
        "After applying all operations in `indices`, return the number of cells in the `m x n` matrix that hold "
        "**odd** values."
    ),
    "cons": [
        "1 <= m, n <= 10^4",
        "0 <= indices.length <= 10^4",
        "indices[i].length == 2",
        "0 <= ri < m, 0 <= ci < n",
    ],
    "hints": [
        "The parity of cell (r, c) depends solely on whether row r was incremented an odd number of times XOR whether column c was incremented an odd number of times.",
        "Track boolean parity arrays for rows and columns; if oddRows rows and oddCols columns have odd parity, the answer is oddRows * (n - oddCols) + (m - oddRows) * oddCols.",
    ],
    "explanations": [
        "After incrementing row 0, col 1 and row 1, col 1, the 2x3 matrix becomes [[1,3,1],[1,3,1]], where all 6 cells are odd.",
        "Row 1 and row 0 each toggle once and col 1 and col 0 each toggle once, making all 4 cells equal to 2 (0 odd cells).",
        "With no operations, every cell stays 0, so there are 0 odd cells.",
    ],
    "time": "O(m + n + len(indices))",
    "space": "O(m + n)",
    "method": "oddCells",
    "params": [("m", "int"), ("n", "int"), ("indices", "int[][]")],
    "ret": "int",
    "py": """        row_odd = [0] * m
        col_odd = [0] * n
        for r, c in indices:
            row_odd[r] ^= 1
            col_odd[c] ^= 1
        ro = sum(row_odd)
        co = sum(col_odd)
        return ro * (n - co) + (m - ro) * co""",
    "java": """        boolean[] rowOdd = new boolean[m];
        boolean[] colOdd = new boolean[n];
        for (int[] idx : indices) {
            rowOdd[idx[0]] = !rowOdd[idx[0]];
            colOdd[idx[1]] = !colOdd[idx[1]];
        }
        int ro = 0, co = 0;
        for (boolean b : rowOdd) if (b) ro++;
        for (boolean b : colOdd) if (b) co++;
        return ro * (n - co) + (m - ro) * co;""",
    "visible": [
        {"m": 2, "n": 3, "indices": [[0, 1], [1, 1]]},
        {"m": 2, "n": 2, "indices": [[1, 1], [0, 0]]},
        {"m": 3, "n": 4, "indices": []},
    ],
    "hidden": [
        {"m": 1, "n": 1, "indices": [[0, 0]]},
        {"m": 1, "n": 1, "indices": [[0, 0], [0, 0]]},
        {"m": 1, "n": 5, "indices": [[0, 2]]},
        {"m": 5, "n": 1, "indices": [[3, 0]]},
        {"m": 3, "n": 3, "indices": [[0, 0], [0, 0], [1, 2]]},
        {"m": 4, "n": 5, "indices": [[0, 1], [2, 3], [0, 4], [3, 1], [2, 3]]},
        {"m": 50, "n": 60, "indices": [[random.Random(8001 + i).randrange(50), random.Random(9001 + i).randrange(60)] for i in range(100)]},
        {"m": 500, "n": 500, "indices": [[(i * 17) % 500, (i * 31) % 500] for i in range(400)]},
        {"m": 10000, "n": 10000, "indices": [[(i * 73) % 10000, (i * 137) % 10000] for i in range(1000)]},
    ],
})

TASKS.append({
    "slug": "81-subrectangle-queries-manager",
    "title": "Subrectangle Queries Manager",
    "difficulty": "Medium",
    "subtopic": "Dynamic Grids",
    "companies": ["Amazon", "Google", "Microsoft", "Atlassian"],
    "desc": (
        "Implement the class `SubrectangleQueries` which receives an `m x n` integer matrix `rectangle` and "
        "supports two operations:\n\n"
        "- `SubrectangleQueries(int[][] rectangle)` initializes the object with the initial matrix.\n"
        "- `void updateSubrectangle(int row1, int col1, int row2, int col2, int newValue)` overwrites every cell "
        "in the subrectangle with upper-left corner `(row1, col1)` and lower-right corner `(row2, col2)` inclusive "
        "with `newValue`.\n"
        "- `int getValue(int row, int col)` returns the current value at coordinate `(row, col)`."
    ),
    "cons": [
        "m == rectangle.length",
        "n == rectangle[i].length",
        "1 <= m, n <= 100",
        "1 <= rectangle[i][j], newValue <= 10^9",
        "0 <= row1 <= row2 < m, 0 <= col1 <= col2 < n",
        "At most 500 operations will be called in total.",
    ],
    "hints": [
        "Instead of rewriting up to m * n cells on every updateSubrectangle call, simply append the tuple (row1, col1, row2, col2, newValue) to an update history list in O(1).",
        "To answer getValue(row, col), scan the history list from newest to oldest and return the first newValue whose bounding box covers (row, col), falling back to the original rectangle.",
    ],
    "explanations": [
        "Initially (0,2)=1; after overwriting [0..3, 0..2] with 5, both (0,2) and (3,1) return 5; then overwriting [3..3, 0..2] with 10 changes (3,1) to 10 while (0,2) remains 5.",
        "Overlapping subrectangle updates resolve in reverse chronological order so the most recent write wins.",
        "On a 1x1 rectangle, each update directly replaces the sole element.",
    ],
    "time": "O(1) update, O(u) query",
    "space": "O(m * n + u)",
    "kind": "design",
    "className": "SubrectangleQueries",
    "constructor": [("rectangle", "int[][]")],
    "methods": [
        ("updateSubrectangle", [("row1", "int"), ("col1", "int"), ("row2", "int"), ("col2", "int"), ("newValue", "int")], "void"),
        ("getValue", [("row", "int"), ("col", "int")], "int"),
    ],
    "py_class": """class SubrectangleQueries:
    def __init__(self, rectangle: List[List[int]]):
        self.rect = [row[:] for row in rectangle]
        self.updates = []

    def updateSubrectangle(self, row1: int, col1: int, row2: int, col2: int, newValue: int) -> None:
        self.updates.append((row1, col1, row2, col2, newValue))

    def getValue(self, row: int, col: int) -> int:
        for r1, c1, r2, c2, val in reversed(self.updates):
            if r1 <= row <= r2 and c1 <= col <= c2:
                return val
        return self.rect[row][col]""",
    "java_class": """class SubrectangleQueries {
    private final int[][] rect;
    private final List<int[]> updates;

    public SubrectangleQueries(int[][] rectangle) {
        this.rect = new int[rectangle.length][];
        for (int i = 0; i < rectangle.length; i++) {
            this.rect[i] = rectangle[i].clone();
        }
        this.updates = new ArrayList<>();
    }

    public void updateSubrectangle(int row1, int col1, int row2, int col2, int newValue) {
        updates.add(new int[]{row1, col1, row2, col2, newValue});
    }

    public int getValue(int row, int col) {
        for (int i = updates.size() - 1; i >= 0; i--) {
            int[] u = updates.get(i);
            if (u[0] <= row && row <= u[2] && u[1] <= col && col <= u[3]) {
                return u[4];
            }
        }
        return rect[row][col];
    }
}""",
    "visible": [
        {
            "ops": ["SubrectangleQueries", "getValue", "updateSubrectangle", "getValue", "getValue", "updateSubrectangle", "getValue", "getValue"],
            "args": [[[[1, 2, 1], [4, 3, 4], [3, 2, 1], [1, 1, 1]]], [0, 2], [0, 0, 3, 2, 5], [0, 2], [3, 1], [3, 0, 3, 2, 10], [3, 1], [0, 2]],
        },
        {
            "ops": ["SubrectangleQueries", "getValue", "updateSubrectangle", "getValue", "getValue", "updateSubrectangle", "getValue"],
            "args": [[[[1, 1, 1], [2, 2, 2], [3, 3, 3]]], [0, 0], [0, 0, 2, 2, 100], [0, 0], [2, 2], [1, 1, 2, 2, 20], [2, 2]],
        },
        {
            "ops": ["SubrectangleQueries", "getValue", "updateSubrectangle", "getValue"],
            "args": [[[[42]]], [0, 0], [0, 0, 0, 0, 99], [0, 0]],
        },
    ],
    "hidden": [
        {
            "ops": ["SubrectangleQueries", "getValue", "getValue"],
            "args": [[[[10, 20, 30], [40, 50, 60]]], [0, 1], [1, 2]],
        },
        {
            "ops": ["SubrectangleQueries", "updateSubrectangle", "updateSubrectangle", "getValue", "getValue"],
            "args": [[[[1, 2, 3, 4]]], [0, 0, 0, 2, 7], [0, 2, 0, 3, 9], [0, 1], [0, 2]],
        },
        {
            "ops": ["SubrectangleQueries", "updateSubrectangle", "getValue", "updateSubrectangle", "getValue"],
            "args": [[[[1], [2], [3], [4]]], [1, 0, 3, 0, 8], [2, 0], [0, 0, 1, 0, 5], [1, 0]],
        },
        {
            "ops": ["SubrectangleQueries", "updateSubrectangle", "updateSubrectangle", "updateSubrectangle", "getValue", "getValue"],
            "args": [[[[1, 2], [3, 4]]], [0, 0, 1, 1, 1000000000], [0, 0, 0, 0, 5], [1, 1, 1, 1, 6], [0, 0], [0, 1]],
        },
        {
            "ops": ["SubrectangleQueries", "updateSubrectangle", "getValue", "getValue", "getValue"],
            "args": [[[[9, 8, 7], [6, 5, 4], [3, 2, 1]]], [1, 1, 1, 1, 999], [0, 0], [1, 1], [2, 2]],
        },
        _rng_subrect_ops(8101, 6, 6, 30),
        _rng_subrect_ops(8102, 12, 15, 80),
        _rng_subrect_ops(8103, 25, 25, 200),
        _rng_subrect_ops(8104, 40, 40, 400),
    ],
})

TASKS.append({
    "slug": "82-sum-of-matrix-after-queries",
    "title": "Sum of Matrix After Queries",
    "difficulty": "Medium",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Amazon", "Meta", "Oracle"],
    "desc": (
        "You are given an integer `n` representing an `n x n` 0-indexed matrix initially filled with all `0`s, "
        "and a 2D array `queries` where each `queries[i] = [type, index, val]`:\n"
        "- If `type == 0`, set every cell in row `index` to `val`, overwriting any previous values.\n"
        "- If `type == 1`, set every cell in column `index` to `val`, overwriting any previous values.\n\n"
        "Return the **sum** of all integers in the matrix after all queries have been applied in order."
    ),
    "cons": [
        "1 <= n <= 10^4",
        "1 <= queries.length <= 5 * 10^4",
        "queries[i].length == 3",
        "type is 0 or 1, 0 <= index < n, 0 <= val <= 10^5",
    ],
    "hints": [
        "Later assignments overwrite earlier ones, so iterate through queries in reverse order (from last to first).",
        "Keep sets (or boolean arrays) of already-finalized rows and columns along with remaining unfinalized counts remRows and remCols: the first time you see a row from the end, it contributes val * remCols to the total sum.",
    ],
    "explanations": [
        "Applying the four queries on a 3x3 matrix produces [[3,1,4],[2,1,4],[2,1,4]], whose elements sum to 23.",
        "The second query overwrites row 0 completely, leaving [[4,4,4],[0,0,0],[0,0,0]] for a sum of 12? Wait: query [1,2,2] sets col 2 to 2 after row 0 is set to 4, giving [[4,4,2],[0,0,2],[0,0,2]] = 14.",
        "On a 1x1 matrix, the last query sets the only cell to 7.",
    ],
    "time": "O(n + q)",
    "space": "O(n)",
    "method": "matrixSumQueries",
    "params": [("n", "int"), ("queries", "int[][]")],
    "ret": "long",
    "py": """        seen_r = [False] * n
        seen_c = [False] * n
        rem_r = n
        rem_c = n
        total = 0
        for qtype, idx, val in reversed(queries):
            if qtype == 0:
                if not seen_r[idx]:
                    seen_r[idx] = True
                    total += val * rem_c
                    rem_r -= 1
            else:
                if not seen_c[idx]:
                    seen_c[idx] = True
                    total += val * rem_r
                    rem_c -= 1
            if rem_r == 0 or rem_c == 0:
                break
        return total""",
    "java": """        boolean[] seenR = new boolean[n];
        boolean[] seenC = new boolean[n];
        int remR = n, remC = n;
        long total = 0;
        for (int i = queries.length - 1; i >= 0; i--) {
            int type = queries[i][0];
            int idx = queries[i][1];
            long val = queries[i][2];
            if (type == 0) {
                if (!seenR[idx]) {
                    seenR[idx] = true;
                    total += val * remC;
                    remR--;
                }
            } else {
                if (!seenC[idx]) {
                    seenC[idx] = true;
                    total += val * remR;
                    remC--;
                }
            }
            if (remR == 0 || remC == 0) break;
        }
        return total;""",
    "visible": [
        {"n": 3, "queries": [[0, 0, 1], [1, 2, 2], [0, 2, 3], [1, 0, 4]]},
        {"n": 3, "queries": [[0, 0, 4], [0, 1, 2], [1, 0, 1], [0, 2, 3], [1, 2, 1]]},
        {"n": 1, "queries": [[0, 0, 3], [1, 0, 7]]},
    ],
    "hidden": [
        {"n": 2, "queries": [[0, 0, 0], [1, 1, 0]]},
        {"n": 3, "queries": [[0, 0, 5], [0, 1, 5], [0, 2, 5]]},
        {"n": 4, "queries": [[1, 0, 10], [1, 1, 20], [1, 2, 30], [1, 3, 40]]},
        {"n": 5, "queries": [[0, 0, 100000], [1, 0, 100000], [0, 4, 100000]]},
        {"n": 10000, "queries": [[0, 0, 100000], [0, 1, 100000], [1, 0, 100000]]},
        {"n": 10000, "queries": [[0, i, 100000] for i in range(100)] + [[1, i, 50000] for i in range(100)]},
        _rng_sum_queries(8201, 20, 60),
        _rng_sum_queries(8202, 200, 400),
        _rng_sum_queries(8203, 5000, 1500),
    ],
})
# Clean up explanations #1 and #2 for problem 82 to match the visible tests accurately!
TASKS[-1]["explanations"][0] = (
    "Processing backwards: col 0 gets 4 (3 cells -> 12), row 2 gets 3 (2 remaining cells -> 6), "
    "col 2 gets 2 (2 remaining cells -> 4), row 0 gets 1 (1 remaining cell -> 1), totaling 23."
)
TASKS[-1]["explanations"][1] = (
    "After applying all five queries in order, the final 3x3 matrix is [[1,4,1],[1,2,1],[1,3,1]], which sums to 17."
)

TASKS.append({
    "slug": "83-matrix-rank-transform",
    "title": "Rank Transform of a Matrix",
    "difficulty": "Hard",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Meta", "Amazon", "Goldman Sachs"],
    "desc": (
        "Given an `m x n` integer matrix `matrix`, return a new `m x n` integer matrix `answer` where "
        "`answer[r][c]` is the **rank** of `matrix[r][c]`.\n\n"
        "The rank is a positive integer starting from `1` computed according to these rules:\n"
        "- If two elements `p` and `q` are in the **same row** or **same column**:\n"
        "  - If `p < q`, then `rank(p) < rank(q)`.\n"
        "  - If `p == q`, then `rank(p) == rank(q)`.\n"
        "- Ranks must be as **small** as possible.\n\n"
        "It is guaranteed that `answer` is unique under these rules."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 200",
        "-10^9 <= matrix[i][j] <= 10^9",
    ],
    "hints": [
        "Process all cells grouped by value in strictly ascending order while maintaining rowMax[r] and colMax[c], the maximum rank assigned so far in each row and column.",
        "Within a single value group, equal elements sharing a row or column must receive the same rank: use Disjoint Set Union (Union-Find) to connect row r with column (m + c) for every cell in the group, then set each connected component's rank to 1 + max(rowMax[r], colMax[c]) across that component.",
    ],
    "explanations": [
        "1 is smallest in its row and column (rank 1); both 2s get rank 2; 3 is larger than both 2s (rank 3), giving [[1,2],[2,3]].",
        "All cells equal 7 and share rows/columns in one connected component, so every cell gets rank 1.",
        "Equal values sharing rows or columns are linked via Union-Find so transitive equal-value chains receive the exact same minimal rank.",
    ],
    "time": "O(m * n * log(m * n))",
    "space": "O(m * n)",
    "method": "matrixRankTransform",
    "params": [("matrix", "int[][]")],
    "ret": "int[][]",
    "py": """        m, n = len(matrix), len(matrix[0])
        groups = defaultdict(list)
        for r in range(m):
            for c in range(n):
                groups[matrix[r][c]].append((r, c))

        row_max = [0] * m
        col_max = [0] * n
        ans = [[0] * n for _ in range(m)]

        for val in sorted(groups):
            parent = {}

            def find(x: int) -> int:
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            cells = groups[val]
            for r, c in cells:
                cc = m + c
                if r not in parent:
                    parent[r] = r
                if cc not in parent:
                    parent[cc] = cc
                ra, rb = find(r), find(cc)
                if ra != rb:
                    parent[ra] = rb

            comp_rank = {}
            for r, c in cells:
                root = find(r)
                prev = row_max[r] if row_max[r] > col_max[c] else col_max[c]
                if root not in comp_rank or prev > comp_rank[root]:
                    comp_rank[root] = prev

            for r, c in cells:
                rank = comp_rank[find(r)] + 1
                ans[r][c] = rank
                row_max[r] = rank
                col_max[c] = rank
        return ans""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        TreeMap<Integer, List<int[]>> groups = new TreeMap<>();
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                groups.computeIfAbsent(matrix[r][c], k -> new ArrayList<>()).add(new int[]{r, c});
            }
        }
        int[] rowMax = new int[m];
        int[] colMax = new int[n];
        int[][] ans = new int[m][n];
        int[] parent = new int[m + n];
        int[] compRank = new int[m + n];

        for (List<int[]> cells : groups.values()) {
            for (int[] cell : cells) {
                int r = cell[0], cc = m + cell[1];
                parent[r] = r;
                parent[cc] = cc;
                compRank[r] = 0;
                compRank[cc] = 0;
            }
            for (int[] cell : cells) {
                int ra = find(parent, cell[0]);
                int rb = find(parent, m + cell[1]);
                if (ra != rb) parent[ra] = rb;
            }
            for (int[] cell : cells) {
                int r = cell[0], c = cell[1];
                int root = find(parent, r);
                int prev = Math.max(rowMax[r], colMax[c]);
                if (prev > compRank[root]) compRank[root] = prev;
            }
            for (int[] cell : cells) {
                int r = cell[0], c = cell[1];
                int rank = compRank[find(parent, r)] + 1;
                ans[r][c] = rank;
                rowMax[r] = rank;
                colMax[c] = rank;
            }
        }
        return ans;""",
    "java_helpers": """    private int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }""",
    "visible": [
        {"matrix": [[1, 2], [3, 4]]},
        {"matrix": [[7, 7], [7, 7]]},
        {"matrix": [[20, -21, 14], [-19, 4, 19], [22, -47, 24], [-19, 4, 19]]},
    ],
    "hidden": [
        {"matrix": [[0]]},
        {"matrix": [[10, 5, 10, 1]]},
        {"matrix": [[10], [5], [10], [1]]},
        {"matrix": [[7, 3, 6], [1, 4, 5], [9, 8, 2]]},
        {"matrix": [[-37, -50, -3, 44], [-37, 46, 13, -32], [47, -42, -3, -40], [-17, -22, -39, 24]]},
        {"matrix": [[5, 1, 5], [1, 5, 1], [5, 1, 5]]},
        {"matrix": [[1000000000, -1000000000], [-1000000000, 1000000000]]},
        {"matrix": _rng_int_grid(8301, 15, 15, -10, 10)},
        {"matrix": _rng_int_grid(8302, 30, 30, -25, 25)},
    ],
})
# Update explanation #1 for problem 83 to match [[1, 2], [3, 4]]!
TASKS[-1]["explanations"][0] = (
    "In [[1,2],[3,4]], 1 gets rank 1; both 2 and 3 exceed 1 in their row/column so they get rank 2; "
    "4 exceeds both 2 and 3, receiving rank 3: [[1,2],[2,3]]."
)


def main() -> None:
    expected_prefixes = list(range(54, 84))
    actual_prefixes = [int(p["slug"].split("-", 1)[0]) for p in TASKS]
    assert actual_prefixes == expected_prefixes, f"Prefix mismatch: {actual_prefixes} != {expected_prefixes}"

    # Scan ALL existing problems globally for slug & title uniqueness
    existing_slugs: dict[str, Path] = {}
    existing_titles: dict[str, Path] = {}
    for p in (ROOT / "problems").rglob("problem.json"):
        folder = p.parent
        m = re.match(r"^(\d{2,3})-(.+)$", folder.name)
        if m:
            existing_slugs[m.group(2)] = folder
        meta = json.loads(p.read_text(encoding="utf-8"))
        existing_titles[meta["title"].lower()] = folder

    for p in TASKS:
        slug_only = p["slug"].split("-", 1)[1]
        folder = BASE / p["slug"]
        if slug_only in existing_slugs and existing_slugs[slug_only] != folder:
            raise AssertionError(f"Duplicate global slug '{slug_only}' (already at {existing_slugs[slug_only]})")
        if p["title"].lower() in existing_titles and existing_titles[p["title"].lower()] != folder:
            raise AssertionError(f"Duplicate global title '{p['title']}' (already at {existing_titles[p['title'].lower()]})")
        existing_slugs[slug_only] = folder
        existing_titles[p["title"].lower()] = folder

        assert len(p["visible"]) == 3, f"{p['slug']} must have 3 visible tests"
        assert len(p["hidden"]) == 9, f"{p['slug']} must have 9 hidden tests"
        assert len(p["explanations"]) == 3, f"{p['slug']} must have 3 example explanations"
        assert len(p["hints"]) == 2, f"{p['slug']} must have 2 hints"

        folder.mkdir(parents=True, exist_ok=True)

        if p.get("kind") == "design":
            sig = {
                "kind": "design",
                "className": p["className"],
                "constructor": {
                    "params": [{"name": n, "type": t} for n, t in p["constructor"]],
                },
                "methods": [
                    {
                        "name": mname,
                        "params": [{"name": n, "type": t} for n, t in mparams],
                        "returns": mret,
                    }
                    for mname, mparams, mret in p["methods"]
                ],
            }
            (folder / "solution.py").write_text(p["py_class"] + "\n", encoding="utf-8")
            (folder / "Solution.java").write_text(p["java_class"] + "\n", encoding="utf-8")
        else:
            params = [{"name": n, "type": t} for n, t in p["params"]]
            sig = {
                "kind": "function",
                "method": p["method"],
                "params": params,
                "returns": p["ret"],
            }
            pyparams = "".join(f", {n}: {py_type(t)}" for n, t in p["params"])
            (folder / "solution.py").write_text(
                f"class Solution:\n    def {p['method']}(self{pyparams}) -> {py_type(p['ret'])}:\n"
                + p["py"]
                + "\n",
                encoding="utf-8",
            )
            jparams = ", ".join(f"{t} {n}" for n, t in p["params"])
            jhelpers = ("\n\n" + p["java_helpers"]) if p.get("java_helpers") else ""
            (folder / "Solution.java").write_text(
                f"class Solution {{\n    public {p['ret']} {p['method']}({jparams}) {{\n"
                + p["java"]
                + "\n    }"
                + jhelpers
                + "\n}\n",
                encoding="utf-8",
            )

        meta = {
            "title": p["title"],
            "difficulty": p["difficulty"],
            "subtopic": p["subtopic"],
            "companies": p["companies"],
            "description": p["desc"],
            "constraints": p["cons"],
            "hints": p["hints"],
            "examples": [{"explanation": e} for e in p["explanations"]],
            "timeComplexity": p["time"],
            "spaceComplexity": p["space"],
            "compare": p.get("compare", "exact"),
            "signature": sig,
        }
        (folder / "problem.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

        vis_code = repr([{"in": x} for x in p["visible"]])
        hid_code = repr([{"in": x} for x in p["hidden"]])
        (folder / "tests.py").write_text(
            f"def visible():\n    return {vis_code}\n\ndef hidden():\n    return {hid_code}\n",
            encoding="utf-8",
        )

    print(f"Generated {len(TASKS)} matrix problems (54-83) in {BASE}")


if __name__ == "__main__":
    main()
