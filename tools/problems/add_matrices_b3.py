#!/usr/bin/env python3
"""Generate matrix problems 84-100 for AlgoPlay (batch 3)."""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "matrices"

ALLOWED_SUBTOPICS = {
    "Spiral Traversal",
    "Matrix Rotation",
    "2D Search",
    "Simulation",
    "Dynamic Grids",
}
ALLOWED_COMPANIES = {
    "Google",
    "Amazon",
    "Microsoft",
    "Meta",
    "Apple",
    "Netflix",
    "Uber",
    "Goldman Sachs",
    "Adobe",
    "Atlassian",
    "Salesforce",
    "Oracle",
    "Bloomberg",
    "LinkedIn",
}


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


def _rng_int_grid(seed: int, m: int, n: int, lo: int, hi: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randint(lo, hi) for _ in range(n)] for _ in range(m)]


def _rng_bin_grid(seed: int, m: int, n: int, p_one: float = 0.5) -> list[list[int]]:
    rng = random.Random(seed)
    return [[1 if rng.random() < p_one else 0 for _ in range(n)] for _ in range(m)]


def _rng_sorted_rows(seed: int, m: int, n: int, lo: int, hi: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [sorted(rng.randint(lo, hi) for _ in range(n)) for _ in range(m)]


def _rng_jagged(seed: int, rows: int, min_len: int, max_len: int, lo: int, hi: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.randint(lo, hi) for _ in range(rng.randint(min_len, max_len))] for _ in range(rows)]


def _rng_periodic_matrix(seed: int, m: int, n: int, period: int, match: bool) -> list[list[int]]:
    rng = random.Random(seed)
    g = []
    for _ in range(m):
        base = [rng.randint(1, 50) for _ in range(period)]
        row = [base[c % period] for c in range(n)]
        g.append(row)
    if not match:
        r = rng.randrange(m)
        c = rng.randrange(n)
        g[r][c] = (g[r][c] % 50) + 1
        if g[r][c] == g[r][(c + period) % n]:
            g[r][c] = (g[r][c] % 50) + 1
    return g


def _warnsdorff_knight_tour(n: int) -> list[list[int]]:
    """Build a valid deterministic n x n knight tour starting at (0, 0)."""
    moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    grid = [[-1] * n for _ in range(n)]
    r, c = 0, 0
    grid[0][0] = 0
    for step in range(1, n * n):
        cands = []
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == -1:
                deg = 0
                for dr2, dc2 in moves:
                    rr, cc = nr + dr2, nc + dc2
                    if 0 <= rr < n and 0 <= cc < n and grid[rr][cc] == -1:
                        deg += 1
                cands.append((deg, nr, nc))
        cands.sort()
        _, r, c = cands[0]
        grid[r][c] = step
    return grid


def _rng_row_col_sums(seed: int, m: int, n: int, max_cell: int) -> dict:
    rng = random.Random(seed)
    mat = [[rng.randint(0, max_cell) for _ in range(n)] for _ in range(m)]
    row_sum = [sum(row) for row in mat]
    col_sum = [sum(mat[r][c] for r in range(m)) for c in range(n)]
    return {"rowSum": row_sum, "colSum": col_sum}


def _rng_unival_grid(seed: int, m: int, n: int, x: int, valid: bool = True) -> dict:
    rng = random.Random(seed)
    rem = rng.randint(1, x)
    max_q = (9999 - rem) // x
    grid = [[rem + x * rng.randint(0, max(1, min(max_q, 40))) for _ in range(n)] for _ in range(m)]
    if not valid and x > 1:
        grid[m // 2][n // 2] += 1
    return {"grid": grid, "x": x}


def _rng_apple_grid(seed: int, m: int, n: int, p_apple: float) -> list[str]:
    rng = random.Random(seed)
    return ["".join("A" if rng.random() < p_apple else "." for _ in range(n)) for _ in range(m)]


TASKS = [
    # ------------------------------------------------------------------
    # 84. Alternating Ring Spiral Traversal (Medium, Spiral Traversal)
    # ------------------------------------------------------------------
    {
        "slug": "84-alternating-ring-spiral-traversal",
        "title": "Alternating Ring Spiral Traversal",
        "difficulty": "Medium",
        "subtopic": "Spiral Traversal",
        "companies": ["Amazon", "Microsoft", "Uber"],
        "desc": (
            "Given an `m x n` integer matrix `matrix`, traverse its concentric rectangular layers from the outermost layer "
            "(layer `0`) inward to the innermost layer and return all visited elements in a single 1D array.\n\n"
            "- Every **even-indexed layer** (`0, 2, 4, ...`) is traversed **clockwise** starting from its top-left corner "
            "`(top, left)`: right along the top edge, down along the right edge, left along the bottom edge (if more than one row), "
            "and up along the left edge (if more than one column).\n"
            "- Every **odd-indexed layer** (`1, 3, 5, ...`) is traversed **counterclockwise** starting from its top-left corner "
            "`(top, left)`: down along the left edge, right along the bottom edge (if more than one column), up along the right edge "
            "(if more than one row and more than one column), and left along the top edge (if more than one row and more than one column)."
        ),
        "cons": [
            "m == matrix.length",
            "n == matrix[i].length",
            "1 <= m, n <= 100",
            "-10^4 <= matrix[i][j] <= 10^4",
        ],
        "hints": [
            "Maintain four layer boundaries (top, bottom, left, right) and a layer counter k, shrinking all four boundaries by 1 after each ring.",
            "When k is odd, handle degenerate 1-row or 1-column inner layers carefully so no cell is visited twice: walk down the left column first, then right across the bottom row only if left < right, and only walk the right and top edges when both top < bottom and left < right.",
        ],
        "explanations": [
            "Layer 0 (outer 4x4 ring) goes clockwise: 1..4, 8, 12, 16..13, 9, 5; layer 1 (inner 2x2 ring) goes counterclockwise from (1,1): 6, 10, 11, 7.",
            "Layer 0 (outer 3x4 ring) goes clockwise around the perimeter; layer 1 is a single-row strip [6, 7], visited left-to-right.",
            "A 3x3 matrix has outer ring clockwise [1,2,3,6,9,8,7,4] and inner single-cell layer [5].",
        ],
        "time": "O(m * n)",
        "space": "O(m * n)",
        "method": "alternatingRingSpiral",
        "params": [("matrix", "int[][]")],
        "ret": "int[]",
        "py": """        m, n = len(matrix), len(matrix[0])
        res = []
        top, bottom, left, right = 0, m - 1, 0, n - 1
        layer = 0
        while top <= bottom and left <= right:
            if layer % 2 == 0:
                for c in range(left, right + 1):
                    res.append(matrix[top][c])
                for r in range(top + 1, bottom + 1):
                    res.append(matrix[r][right])
                if top < bottom:
                    for c in range(right - 1, left - 1, -1):
                        res.append(matrix[bottom][c])
                if left < right:
                    for r in range(bottom - 1, top, -1):
                        res.append(matrix[r][left])
            else:
                for r in range(top, bottom + 1):
                    res.append(matrix[r][left])
                if left < right:
                    for c in range(left + 1, right + 1):
                        res.append(matrix[bottom][c])
                if top < bottom and left < right:
                    for r in range(bottom - 1, top - 1, -1):
                        res.append(matrix[r][right])
                    for c in range(right - 1, left, -1):
                        res.append(matrix[top][c])
            top += 1
            bottom -= 1
            left += 1
            right -= 1
            layer += 1
        return res""",
        "java": """        int m = matrix.length, n = matrix[0].length;
        int[] res = new int[m * n];
        int idx = 0;
        int top = 0, bottom = m - 1, left = 0, right = n - 1;
        int layer = 0;
        while (top <= bottom && left <= right) {
            if (layer % 2 == 0) {
                for (int c = left; c <= right; c++) res[idx++] = matrix[top][c];
                for (int r = top + 1; r <= bottom; r++) res[idx++] = matrix[r][right];
                if (top < bottom) {
                    for (int c = right - 1; c >= left; c--) res[idx++] = matrix[bottom][c];
                }
                if (left < right) {
                    for (int r = bottom - 1; r > top; r--) res[idx++] = matrix[r][left];
                }
            } else {
                for (int r = top; r <= bottom; r++) res[idx++] = matrix[r][left];
                if (left < right) {
                    for (int c = left + 1; c <= right; c++) res[idx++] = matrix[bottom][c];
                }
                if (top < bottom && left < right) {
                    for (int r = bottom - 1; r >= top; r--) res[idx++] = matrix[r][right];
                    for (int c = right - 1; c > left; c--) res[idx++] = matrix[top][c];
                }
            }
            top++;
            bottom--;
            left++;
            right--;
            layer++;
        }
        return res;""",
        "visible": [
            {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]},
            {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]},
            {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        ],
        "hidden": [
            {"matrix": [[42]]},
            {"matrix": [[1, 2, 3, 4, 5]]},
            {"matrix": [[1], [2], [3], [4], [5]]},
            {"matrix": [[1, 2], [3, 4]]},
            {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]},
            {"matrix": [[r * 5 + c + 1 for c in range(5)] for r in range(5)]},
            {"matrix": [[r * 6 + c + 1 for c in range(6)] for r in range(6)]},
            {"matrix": _rng_int_grid(8401, 7, 10, -100, 100)},
            {"matrix": _rng_int_grid(8402, 25, 28, -5000, 5000)},
        ],
    },
    # ------------------------------------------------------------------
    # 85. Diagonal Traverse of Jagged Matrix (Medium, Spiral Traversal)
    # ------------------------------------------------------------------
    {
        "slug": "85-diagonal-traverse-variable-rows",
        "title": "Diagonal Traverse of Jagged Matrix",
        "difficulty": "Medium",
        "subtopic": "Spiral Traversal",
        "companies": ["Meta", "Google", "Amazon", "Apple"],
        "desc": (
            "Given a 2D list of integers `nums` where each row may have a **different** positive length (a jagged matrix), "
            "return all elements of `nums` in anti-diagonal order as a 1D integer array.\n\n"
            "Elements are ordered by increasing diagonal sum `r + c`. Within the same diagonal `r + c`, elements are ordered "
            "from the **bottom-most row to the top-most row** (decreasing `r`, equivalently increasing `c`)."
        ),
        "cons": [
            "1 <= nums.length <= 10^4",
            "1 <= nums[i].length <= 10^4",
            "1 <= sum(nums[i].length) <= 10^4",
            "-10^5 <= nums[i][j] <= 10^5",
        ],
        "hints": [
            "Iterating over the full bounding box of maxRows x maxCols wastes time on empty gaps when rows vary wildly in length.",
            "Notice that every cell (r, c) belongs to diagonal d = r + c; if you iterate rows from bottom to top (m - 1 down to 0) and append nums[r][c] to bucket[r + c], every bucket is already in exact bottom-to-top order in O(N) total time.",
        ],
        "explanations": [
            "Diagonals by r + c are: [1], [4, 2], [7, 5, 3], [8, 6], [9].",
            "Even with ragged row lengths, cells sharing r + c are grouped from larger row index to smaller row index.",
            "A single row produces its elements unchanged from left to right.",
        ],
        "time": "O(N)",
        "space": "O(N)",
        "method": "findDiagonalOrder",
        "params": [("nums", "List<List<Integer>>")],
        "ret": "int[]",
        "py": """        buckets = []
        total = 0
        for r in range(len(nums) - 1, -1, -1):
            row = nums[r]
            total += len(row)
            for c, val in enumerate(row):
                d = r + c
                while len(buckets) <= d:
                    buckets.append([])
                buckets[d].append(val)
        res = []
        for b in buckets:
            res.extend(b)
        return res""",
        "java": """        List<List<Integer>> buckets = new ArrayList<>();
        int total = 0;
        for (int r = nums.size() - 1; r >= 0; r--) {
            List<Integer> row = nums.get(r);
            total += row.size();
            for (int c = 0; c < row.size(); c++) {
                int d = r + c;
                while (buckets.size() <= d) {
                    buckets.add(new ArrayList<>());
                }
                buckets.get(d).add(row.get(c));
            }
        }
        int[] res = new int[total];
        int idx = 0;
        for (List<Integer> b : buckets) {
            for (int v : b) {
                res[idx++] = v;
            }
        }
        return res;""",
        "visible": [
            {"nums": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
            {"nums": [[1, 2, 3, 4, 5], [6, 7], [8], [9, 10, 11], [12, 13, 14, 15, 16]]},
            {"nums": [[10, 20, 30, 40]]},
        ],
        "hidden": [
            {"nums": [[7]]},
            {"nums": [[1], [2], [3], [4], [5]]},
            {"nums": [[1, 2, 3, 4, 5, 6], [7], [8], [9], [10, 11]]},
            {"nums": [[1], [2, 3], [4, 5, 6], [7, 8, 9, 10]]},
            {"nums": [[1, 2, 3, 4], [5, 6, 7], [8, 9], [10]]},
            {"nums": [[-5, 0], [3, -2, 8], [-1], [4, 9, -7, 2]]},
            {"nums": [[i + 1] for i in range(40)] + [[100 + j for j in range(40)]]},
            {"nums": _rng_jagged(8501, 25, 1, 15, -500, 500)},
            {"nums": _rng_jagged(8502, 80, 1, 25, -10000, 10000)},
        ],
    },
    # ------------------------------------------------------------------
    # 86. Matrix Cells in Distance Order (Easy, Spiral Traversal)
    # ------------------------------------------------------------------
    {
        "slug": "86-matrix-cells-in-distance-order",
        "title": "Matrix Cells in Distance Order",
        "difficulty": "Easy",
        "subtopic": "Spiral Traversal",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": (
            "You are given four integers `rows`, `cols`, `rCenter`, and `cCenter` describing a `rows x cols` matrix and a "
            "center cell `(rCenter, cCenter)`.\n\n"
            "Return a 2D array containing the `[r, c]` coordinates of every cell in the matrix, ordered by increasing "
            "**Manhattan distance** `|r - rCenter| + |c - cCenter|` from `(rCenter, cCenter)`. If two cells have the same "
            "Manhattan distance, order them by smaller row `r`, and if rows are equal, by smaller column `c`."
        ),
        "cons": [
            "1 <= rows, cols <= 100",
            "0 <= rCenter < rows",
            "0 <= cCenter < cols",
        ],
        "hints": [
            "The maximum possible Manhattan distance from (rCenter, cCenter) is at most (rows - 1) + (cols - 1).",
            "Bucket all coordinates by their Manhattan distance while scanning r from 0 to rows - 1 and c from 0 to cols - 1; each bucket automatically respects the (r, c) tie-breaking order in O(rows * cols) time.",
        ],
        "explanations": [
            "From (0, 0) in a 1x2 grid, distances are 0 at (0, 0) and 1 at (0, 1).",
            "From (0, 1) in a 2x2 grid, (0, 1) has distance 0, (0, 0) and (1, 1) have distance 1 (ordered by row), and (1, 0) has distance 2.",
            "From (1, 2) in a 2x3 grid, cells are grouped by Manhattan shells 0, 1, 2, 3 with row-major tie-breaking.",
        ],
        "time": "O(rows * cols)",
        "space": "O(rows * cols)",
        "method": "allCellsDistOrder",
        "params": [("rows", "int"), ("cols", "int"), ("rCenter", "int"), ("cCenter", "int")],
        "ret": "int[][]",
        "py": """        max_d = max(rCenter, rows - 1 - rCenter) + max(cCenter, cols - 1 - cCenter)
        buckets = [[] for _ in range(max_d + 1)]
        for r in range(rows):
            dr = abs(r - rCenter)
            for c in range(cols):
                buckets[dr + abs(c - cCenter)].append([r, c])
        res = []
        for b in buckets:
            res.extend(b)
        return res""",
        "java": """        int maxD = Math.max(rCenter, rows - 1 - rCenter) + Math.max(cCenter, cols - 1 - cCenter);
        List<List<int[]>> buckets = new ArrayList<>(maxD + 1);
        for (int d = 0; d <= maxD; d++) buckets.add(new ArrayList<>());
        for (int r = 0; r < rows; r++) {
            int dr = Math.abs(r - rCenter);
            for (int c = 0; c < cols; c++) {
                buckets.get(dr + Math.abs(c - cCenter)).add(new int[]{r, c});
            }
        }
        int[][] res = new int[rows * cols][2];
        int idx = 0;
        for (List<int[]> b : buckets) {
            for (int[] cell : b) {
                res[idx++] = cell;
            }
        }
        return res;""",
        "visible": [
            {"rows": 1, "cols": 2, "rCenter": 0, "cCenter": 0},
            {"rows": 2, "cols": 2, "rCenter": 0, "cCenter": 1},
            {"rows": 2, "cols": 3, "rCenter": 1, "cCenter": 2},
        ],
        "hidden": [
            {"rows": 1, "cols": 1, "rCenter": 0, "cCenter": 0},
            {"rows": 3, "cols": 3, "rCenter": 1, "cCenter": 1},
            {"rows": 4, "cols": 1, "rCenter": 2, "cCenter": 0},
            {"rows": 1, "cols": 5, "rCenter": 0, "cCenter": 3},
            {"rows": 4, "cols": 4, "rCenter": 0, "cCenter": 0},
            {"rows": 4, "cols": 4, "rCenter": 3, "cCenter": 3},
            {"rows": 5, "cols": 6, "rCenter": 2, "cCenter": 4},
            {"rows": 10, "cols": 10, "rCenter": 4, "cCenter": 6},
            {"rows": 20, "cols": 25, "rCenter": 9, "cCenter": 12},
        ],
    },
    # ------------------------------------------------------------------
    # 87. Maximal Upper-Left Quadrant Sum by Flips (Medium, Matrix Rotation)
    # ------------------------------------------------------------------
    {
        "slug": "87-flip-matrix-for-maximal-quadrant-sum",
        "title": "Maximal Upper-Left Quadrant Sum by Flips",
        "difficulty": "Medium",
        "subtopic": "Matrix Rotation",
        "companies": ["Goldman Sachs", "Google", "Amazon", "Bloomberg"],
        "desc": (
            "You are given a `2n x 2n` integer matrix `matrix`. In a single operation, you may reverse any entire row "
            "(left-to-right) or reverse any entire column (top-to-bottom). You may perform as many operations as you wish in any order.\n\n"
            "Return the **maximum possible sum** of the elements in the `n x n` upper-left quadrant `matrix[0..n-1][0..n-1]`."
        ),
        "cons": [
            "matrix.length == 2 * n",
            "matrix[i].length == 2 * n",
            "1 <= n <= 100",
            "-10^9 <= matrix[i][j] <= 10^9",
        ],
        "hints": [
            "Reversing rows and columns can only swap cell (r, c) among the four mirror-symmetric positions: (r, c), (r, 2n - 1 - c), (2n - 1 - r, c), and (2n - 1 - r, 2n - 1 - c).",
            "Every cell in the upper-left n x n quadrant can independently achieve the maximum of its 4-cell symmetry orbit without disturbing the other orbits.",
        ],
        "explanations": [
            "For the single upper-left cell (0, 0), the maximum of {1, 2, 3, 4} is 4 (reverse row 1 then column 0).",
            "Each of the 4 upper-left cells picks the largest value in its 4-corner symmetry group: 119 + 114 + 56 + 125 = 414.",
            "Negative values work identically: each orbit selects its least negative member, giving -10 + -1 + -3 + -30 = -44.",
        ],
        "time": "O(n^2)",
        "space": "O(1)",
        "method": "maxQuadrantSum",
        "params": [("matrix", "int[][]")],
        "ret": "long",
        "py": """        m = len(matrix)
        n = m // 2
        total = 0
        for r in range(n):
            mr = m - 1 - r
            for c in range(n):
                mc = m - 1 - c
                total += max(matrix[r][c], matrix[r][mc], matrix[mr][c], matrix[mr][mc])
        return total""",
        "java": """        int m = matrix.length;
        int n = m / 2;
        long total = 0;
        for (int r = 0; r < n; r++) {
            int mr = m - 1 - r;
            for (int c = 0; c < n; c++) {
                int mc = m - 1 - c;
                int best = Math.max(
                    Math.max(matrix[r][c], matrix[r][mc]),
                    Math.max(matrix[mr][c], matrix[mr][mc])
                );
                total += best;
            }
        }
        return total;""",
        "visible": [
            {"matrix": [[1, 2], [3, 4]]},
            {
                "matrix": [
                    [112, 42, 83, 119],
                    [56, 125, 56, 49],
                    [15, 78, 101, 43],
                    [62, 98, 114, 108],
                ]
            },
            {
                "matrix": [
                    [-10, -1, -2, -20],
                    [-3, -30, -40, -4],
                    [-50, -60, -70, -80],
                    [-90, -100, -110, -120],
                ]
            },
        ],
        "hidden": [
            {"matrix": [[0, 0], [0, 0]]},
            {"matrix": [[1000000000, -1000000000], [-1000000000, 1000000000]]},
            {"matrix": [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]]},
            {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]},
            {"matrix": _rng_int_grid(8701, 6, 6, -100, 100)},
            {"matrix": _rng_int_grid(8702, 8, 8, 0, 1000)},
            {"matrix": _rng_int_grid(8703, 12, 12, -1000000000, 1000000000)},
            {"matrix": _rng_int_grid(8704, 20, 20, -5000, 5000)},
            {"matrix": _rng_int_grid(8705, 36, 36, -1000000000, 1000000000)},
        ],
    },
    # ------------------------------------------------------------------
    # 88. Matrix Similarity After Cyclic Shifts (Easy, Matrix Rotation)
    # ------------------------------------------------------------------
    {
        "slug": "88-matrix-similarity-after-cyclic-shifts",
        "title": "Matrix Similarity After Cyclic Shifts",
        "difficulty": "Easy",
        "subtopic": "Matrix Rotation",
        "companies": ["Amazon", "Adobe", "Oracle"],
        "desc": (
            "You are given an `m x n` integer matrix `mat` and a non-negative integer `k`. Perform the following step `k` times:\n"
            "- Shift every **even-indexed row** (`0, 2, 4, ...`) cyclically **left** by `1` position.\n"
            "- Shift every **odd-indexed row** (`1, 3, 5, ...`) cyclically **right** by `1` position.\n\n"
            "Return `true` if the matrix obtained after all `k` steps is identical to the initial matrix `mat`, and `false` otherwise."
        ),
        "cons": [
            "m == mat.length",
            "n == mat[i].length",
            "1 <= m, n <= 50",
            "1 <= mat[i][j] <= 100",
            "0 <= k <= 10^9",
        ],
        "hints": [
            "Shifting a row of length n by k steps only depends on shift = k % n.",
            "A row is unchanged under a cyclic left shift by shift if and only if it is unchanged under a cyclic right shift by shift: simply check mat[r][c] == mat[r][(c + shift) % n] for every cell.",
        ],
        "explanations": [
            "Each row has length 4 and repeats every 2 positions, so shifting by k = 2 leaves every row unchanged.",
            "Row [1, 2, 1, 2] is periodic with period 2, but k = 1 shifts it to [2, 1, 2, 1], which differs from the original.",
            "With k = 3 on a 3-column matrix, k % 3 == 0 so every row completes a full rotation and matches.",
        ],
        "time": "O(m * n)",
        "space": "O(1)",
        "method": "areSimilarAfterShifts",
        "params": [("mat", "int[][]"), ("k", "int")],
        "ret": "boolean",
        "py": """        n = len(mat[0])
        shift = k % n
        if shift == 0:
            return True
        for row in mat:
            for c in range(n):
                if row[c] != row[(c + shift) % n]:
                    return False
        return True""",
        "java": """        int n = mat[0].length;
        int shift = k % n;
        if (shift == 0) return true;
        for (int[] row : mat) {
            for (int c = 0; c < n; c++) {
                if (row[c] != row[(c + shift) % n]) {
                    return false;
                }
            }
        }
        return true;""",
        "visible": [
            {"mat": [[1, 2, 1, 2], [5, 5, 5, 5], [6, 3, 6, 3]], "k": 2},
            {"mat": [[1, 2, 1, 2], [5, 5, 5, 5], [6, 3, 6, 3]], "k": 1},
            {"mat": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "k": 3},
        ],
        "hidden": [
            {"mat": [[42]], "k": 1000000000},
            {"mat": [[1, 2, 3]], "k": 0},
            {"mat": [[1, 2], [3, 4]], "k": 1},
            {"mat": [[2, 2], [2, 2]], "k": 999999999},
            {"mat": [[1, 2, 3, 1, 2, 3], [4, 5, 6, 4, 5, 6]], "k": 9},
            {"mat": [[1, 2, 3, 1, 2, 3], [4, 5, 6, 4, 5, 7]], "k": 3},
            {"mat": _rng_periodic_matrix(8801, 15, 12, 4, True), "k": 100000000},
            {"mat": _rng_periodic_matrix(8802, 15, 12, 4, False), "k": 100000000},
            {"mat": _rng_periodic_matrix(8803, 40, 36, 6, True), "k": 999999996},
        ],
    },
    # ------------------------------------------------------------------
    # 89. Minimum Operations for 90-Degree Rotational Symmetry (Medium, Matrix Rotation)
    # ------------------------------------------------------------------
    {
        "slug": "89-minimum-ops-for-rotational-symmetry",
        "title": "Minimum Operations for 90-Degree Rotational Symmetry",
        "difficulty": "Medium",
        "subtopic": "Matrix Rotation",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": (
            "You are given an `n x n` integer matrix `grid`. In one operation, you may choose any cell `(r, c)` and either "
            "increment `grid[r][c]` by `1` or decrement `grid[r][c]` by `1`.\n\n"
            "Return the **minimum total number of operations** required so that `grid` becomes identical to its own "
            "`90`-degree clockwise rotation (i.e., `grid[r][c] == grid[c][n - 1 - r]` for all `0 <= r, c < n`)."
        ),
        "cons": [
            "n == grid.length == grid[i].length",
            "1 <= n <= 200",
            "-10^9 <= grid[i][j] <= 10^9",
        ],
        "hints": [
            "Under 90-degree clockwise rotation, the matrix splits into disjoint 4-cell orbits {(r, c), (c, n-1-r), (n-1-r, n-1-c), (n-1-c, r)}, plus an invariant center cell when n is odd.",
            "All four values in an orbit must be made equal; for sorted values a <= b <= c <= d, the minimum L1 cost is achieved at any target in [b, c] and equals (d - a) + (c - b).",
        ],
        "explanations": [
            "All four cells form one orbit [1, 2, 3, 4]; bringing them to 2 or 3 costs (4 - 1) + (3 - 2) = 4.",
            "The matrix is already invariant under 90-degree clockwise rotation, requiring 0 operations.",
            "Corner orbit [1, 5, 1, 5] costs 8, edge orbit [2, 2, 6, 2] costs 4, and the center cell 9 is invariant, totaling 12.",
        ],
        "time": "O(n^2)",
        "space": "O(1)",
        "method": "minOpsRotationalSymmetry",
        "params": [("grid", "int[][]")],
        "ret": "long",
        "py": """        n = len(grid)
        ops = 0
        for r in range(n // 2):
            for c in range((n + 1) // 2):
                vals = [
                    grid[r][c],
                    grid[c][n - 1 - r],
                    grid[n - 1 - r][n - 1 - c],
                    grid[n - 1 - c][r],
                ]
                vals.sort()
                ops += (vals[3] - vals[0]) + (vals[2] - vals[1])
        return ops""",
        "java": """        int n = grid.length;
        long ops = 0;
        int[] vals = new int[4];
        for (int r = 0; r < n / 2; r++) {
            for (int c = 0; c < (n + 1) / 2; c++) {
                vals[0] = grid[r][c];
                vals[1] = grid[c][n - 1 - r];
                vals[2] = grid[n - 1 - r][n - 1 - c];
                vals[3] = grid[n - 1 - c][r];
                Arrays.sort(vals);
                ops += ((long) vals[3] - vals[0]) + ((long) vals[2] - vals[1]);
            }
        }
        return ops;""",
        "visible": [
            {"grid": [[1, 2], [4, 3]]},
            {"grid": [[5, 2, 5], [2, 9, 2], [5, 2, 5]]},
            {"grid": [[1, 2, 5], [2, 9, 2], [5, 6, 1]]},
        ],
        "hidden": [
            {"grid": [[99]]},
            {"grid": [[0, 0], [0, 0]]},
            {"grid": [[-1000000000, 1000000000], [1000000000, -1000000000]]},
            {"grid": [[1, 1, 1, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 1, 1, 1]]},
            {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]},
            {"grid": _rng_int_grid(8901, 5, 5, -50, 50)},
            {"grid": _rng_int_grid(8902, 11, 11, -1000, 1000)},
            {"grid": _rng_int_grid(8903, 20, 20, -1000000000, 1000000000)},
            {"grid": _rng_int_grid(8904, 35, 35, -1000000000, 1000000000)},
        ],
    },
    # ------------------------------------------------------------------
    # 90. Maximum Diagonal Sum by Ring Rotations (Hard, Matrix Rotation)
    # ------------------------------------------------------------------
    {
        "slug": "90-maximum-diagonal-sum-by-ring-rotations",
        "title": "Maximum Diagonal Sum by Ring Rotations",
        "difficulty": "Hard",
        "subtopic": "Matrix Rotation",
        "companies": ["Google", "Goldman Sachs", "Uber", "Meta"],
        "desc": (
            "You are given an `n x n` integer matrix `matrix`. Before computing the sum of its two main diagonals, you may "
            "independently rotate **each concentric square ring** of `matrix` clockwise by any non-negative number of positions "
            "(rotating a ring shifts only the perimeter cells of that ring along its cyclic boundary).\n\n"
            "Return the **maximum possible sum** of all cells lying on the primary diagonal (`r == c`) or the secondary diagonal "
            "(`r + c == n - 1`), counting the center cell once when `n` is odd."
        ),
        "cons": [
            "n == matrix.length == matrix[i].length",
            "1 <= n <= 200",
            "-10^9 <= matrix[i][j] <= 10^9",
        ],
        "hints": [
            "Concentric rings can be rotated completely independently, and each ring k of side length L = n - 2k >= 2 contributes exactly its 4 corner cells to the two diagonals.",
            "In cyclic order around ring k, the 4 corner slots are spaced S = L - 1 positions apart, so any rotation places the quadruple {(k, k+i), (k+i, k+S), (k+S, k+S-i), (k+S-i, k)} onto the corners for some 0 <= i < S.",
        ],
        "explanations": [
            "Rotating the outer 3x3 ring by 1 step moves the four edge midpoints (10, 10, 10, 10) onto the four corners; adding the center cell 5 gives 45.",
            "In a 2x2 matrix, all four cells always lie on the diagonals regardless of rotation: 1 + 2 + 3 + 4 = 10.",
            "In a 4x4 matrix, outer ring picks the best of 3 phases and inner 2x2 ring always contributes all 4 of its cells.",
        ],
        "time": "O(n^2)",
        "space": "O(1)",
        "method": "maxDiagonalSumAfterRingRotations",
        "params": [("matrix", "int[][]")],
        "ret": "long",
        "py": """        n = len(matrix)
        ans = matrix[n // 2][n // 2] if n % 2 == 1 else 0
        for k in range(n // 2):
            s = n - 1 - 2 * k
            best = None
            for i in range(s):
                cur = (
                    matrix[k][k + i]
                    + matrix[k + i][k + s]
                    + matrix[k + s][k + s - i]
                    + matrix[k + s - i][k]
                )
                if best is None or cur > best:
                    best = cur
            ans += best
        return ans""",
        "java": """        int n = matrix.length;
        long ans = (n % 2 == 1) ? matrix[n / 2][n / 2] : 0L;
        for (int k = 0; k < n / 2; k++) {
            int s = n - 1 - 2 * k;
            long best = Long.MIN_VALUE;
            for (int i = 0; i < s; i++) {
                long cur = (long) matrix[k][k + i]
                    + matrix[k + i][k + s]
                    + matrix[k + s][k + s - i]
                    + matrix[k + s - i][k];
                if (cur > best) best = cur;
            }
            ans += best;
        }
        return ans;""",
        "visible": [
            {"matrix": [[1, 10, 1], [10, 5, 10], [1, 10, 1]]},
            {"matrix": [[1, 2], [3, 4]]},
            {"matrix": [[1, 9, 2, 1], [2, 3, 4, 9], [9, 5, 6, 2], [1, 2, 9, 1]]},
        ],
        "hidden": [
            {"matrix": [[-7]]},
            {"matrix": [[-10, -1, -10], [-1, -5, -1], [-10, -1, -10]]},
            {"matrix": [[1000000000, -1000000000, 1000000000], [-1000000000, 1000000000, -1000000000], [1000000000, -1000000000, 1000000000]]},
            {"matrix": [[r * 5 + c + 1 for c in range(5)] for r in range(5)]},
            {"matrix": [[0] * 6 for _ in range(6)]},
            {"matrix": _rng_int_grid(9001, 7, 7, -100, 100)},
            {"matrix": _rng_int_grid(9002, 10, 10, -500, 500)},
            {"matrix": _rng_int_grid(9003, 21, 21, -1000000000, 1000000000)},
            {"matrix": _rng_int_grid(9004, 36, 36, -1000000000, 1000000000)},
        ],
    },
    # ------------------------------------------------------------------
    # 91. Median of a Row-Wise Sorted Matrix (Medium, 2D Search)
    # ------------------------------------------------------------------
    {
        "slug": "91-median-of-row-wise-sorted-matrix",
        "title": "Median of a Row-Wise Sorted Matrix",
        "difficulty": "Medium",
        "subtopic": "2D Search",
        "companies": ["Google", "Amazon", "Microsoft", "Bloomberg"],
        "desc": (
            "Given an `m x n` integer matrix `grid` where **both `m` and `n` are odd** and every row is sorted in "
            "**non-decreasing** order, return the **median** of all `m * n` elements in the matrix.\n\n"
            "Because `m * n` is guaranteed to be odd, the median is the unique middle element at 0-based index `(m * n) // 2` "
            "when all elements of `grid` are sorted."
        ),
        "cons": [
            "m == grid.length, n == grid[i].length",
            "1 <= m, n <= 300",
            "m and n are both odd integers.",
            "-10^9 <= grid[i][j] <= 10^9",
            "Every row grid[r] is sorted in non-decreasing order.",
        ],
        "hints": [
            "Binary search on the value range [min(first column), max(last column)] instead of flattening and sorting all m * n elements.",
            "For any candidate value mid, count how many elements across all rows are <= mid using binary search (upper bound) in each sorted row; the median is the smallest mid whose count is at least (m * n + 1) / 2.",
        ],
        "explanations": [
            "All elements sorted are [1, 2, 3, 3, 5, 6, 6, 9, 9]; the middle (5th) element is 5.",
            "Sorted elements are [1, 1, 2, 2, 3, 3, 4, 5, 6]; the 5th element is 3.",
            "A 1x5 sorted row has its median directly at index 2, which is -2.",
        ],
        "time": "O(m * log n * log(maxVal - minVal))",
        "space": "O(1)",
        "method": "matrixMedian",
        "params": [("grid", "int[][]")],
        "ret": "int",
        "py": """        import bisect
        m, n = len(grid), len(grid[0])
        lo = min(row[0] for row in grid)
        hi = max(row[-1] for row in grid)
        need = (m * n + 1) // 2
        while lo < hi:
            mid = lo + (hi - lo) // 2
            cnt = 0
            for row in grid:
                cnt += bisect.bisect_right(row, mid)
            if cnt >= need:
                hi = mid
            else:
                lo = mid + 1
        return lo""",
        "java": """        int m = grid.length, n = grid[0].length;
        long lo = grid[0][0], hi = grid[0][n - 1];
        for (int r = 1; r < m; r++) {
            if (grid[r][0] < lo) lo = grid[r][0];
            if (grid[r][n - 1] > hi) hi = grid[r][n - 1];
        }
        int need = (m * n + 1) / 2;
        while (lo < hi) {
            long mid = lo + (hi - lo) / 2;
            int cnt = 0;
            for (int[] row : grid) {
                int l = 0, r = n;
                while (l < r) {
                    int k = (l + r) >>> 1;
                    if (row[k] <= mid) l = k + 1;
                    else r = k;
                }
                cnt += l;
            }
            if (cnt >= need) hi = mid;
            else lo = mid + 1;
        }
        return (int) lo;""",
        "visible": [
            {"grid": [[1, 3, 5], [2, 6, 9], [3, 6, 9]]},
            {"grid": [[1, 1, 2], [2, 3, 3], [4, 5, 6]]},
            {"grid": [[-10, -5, -2, 4, 8]]},
        ],
        "hidden": [
            {"grid": [[42]]},
            {"grid": [[7], [-3], [15], [0], [2]]},
            {"grid": [[5, 5, 5], [5, 5, 5], [5, 5, 5]]},
            {"grid": [[-1000000000, 0, 1000000000], [-1000000000, -1, 1000000000], [-500, 500, 1000000000]]},
            {"grid": [[1, 2, 3], [1, 2, 3], [1, 2, 3]]},
            {"grid": _rng_sorted_rows(9101, 5, 7, -100, 100)},
            {"grid": _rng_sorted_rows(9102, 9, 9, -1000000, 1000000)},
            {"grid": _rng_sorted_rows(9103, 15, 19, -1000000000, 1000000000)},
            {"grid": _rng_sorted_rows(9104, 31, 31, -1000000000, 1000000000)},
        ],
    },
    # ------------------------------------------------------------------
    # 92. Kth Smallest Sum of a Matrix With Sorted Rows (Hard, 2D Search)
    # ------------------------------------------------------------------
    {
        "slug": "92-kth-smallest-sum-of-matrix-rows",
        "title": "Kth Smallest Sum of a Matrix With Sorted Rows",
        "difficulty": "Hard",
        "subtopic": "2D Search",
        "companies": ["Google", "Meta", "Amazon", "Salesforce"],
        "desc": (
            "You are given an `m x n` integer matrix `mat` where each row is sorted in **non-decreasing** order, along with "
            "a positive integer `k`.\n\n"
            "You may choose exactly one element from each row to form an array of length `m`. Return the **`k`-th smallest** "
            "possible sum among all `n^m` such arrays (1-indexed, counting duplicate sums with multiplicity)."
        ),
        "cons": [
            "m == mat.length, n == mat[i].length",
            "1 <= m, n <= 40",
            "1 <= k <= min(200, n^m)",
            "1 <= mat[i][j] <= 5000",
            "Every row mat[i] is sorted in non-decreasing order.",
        ],
        "hints": [
            "Merge rows one at a time, keeping only the k smallest prefix sums after each row because larger prefix sums can never participate in the global top-k sums.",
            "To merge two sorted arrays A (size <= k) and B (size n) into their k smallest pairwise sums, push (A[i] + B[0], i, 0) into a min-heap and pop k times, advancing j to j + 1 on each pop.",
        ],
        "explanations": [
            "Choosing one element from each of [1,3,11] and [2,4,6] gives smallest sums 3, 5, 5, 7, 7; the 5th smallest is 7.",
            "With k = 9, all 3x3 = 9 pair sums are [3, 5, 5, 7, 7, 9, 13, 15, 17]; the 9th smallest is 17.",
            "Across 3 rows, the 7 smallest combination sums are 7, 9, 9, 9, 9, 9, 9; the 7th is 9.",
        ],
        "time": "O(m * k * log k)",
        "space": "O(k)",
        "method": "kthSmallestRowSum",
        "params": [("mat", "int[][]"), ("k", "int")],
        "ret": "int",
        "py": """        cur = mat[0][:k]
        for row in mat[1:]:
            heap = [(cur[i] + row[0], i, 0) for i in range(len(cur))]
            heapq.heapify(heap)
            nxt = []
            while heap and len(nxt) < k:
                s, i, j = heapq.heappop(heap)
                nxt.append(s)
                if j + 1 < len(row):
                    heapq.heappush(heap, (cur[i] + row[j + 1], i, j + 1))
            cur = nxt
        return cur[k - 1]""",
        "java": """        int m = mat.length, n = mat[0].length;
        int len = Math.min(n, k);
        int[] cur = Arrays.copyOf(mat[0], len);
        for (int r = 1; r < m; r++) {
            int[] row = mat[r];
            PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
            for (int i = 0; i < cur.length; i++) {
                pq.offer(new int[]{cur[i] + row[0], i, 0});
            }
            int limit = Math.min(k, cur.length * n);
            int[] nxt = new int[limit];
            int idx = 0;
            while (!pq.isEmpty() && idx < limit) {
                int[] top = pq.poll();
                nxt[idx++] = top[0];
                int i = top[1], j = top[2];
                if (j + 1 < n) {
                    pq.offer(new int[]{cur[i] + row[j + 1], i, j + 1});
                }
            }
            cur = nxt;
        }
        return cur[k - 1];""",
        "visible": [
            {"mat": [[1, 3, 11], [2, 4, 6]], "k": 5},
            {"mat": [[1, 3, 11], [2, 4, 6]], "k": 9},
            {"mat": [[1, 10, 10], [1, 4, 5], [2, 3, 6]], "k": 7},
        ],
        "hidden": [
            {"mat": [[5]], "k": 1},
            {"mat": [[2, 4, 6, 8]], "k": 3},
            {"mat": [[10], [20], [30]], "k": 1},
            {"mat": [[1, 1, 10], [2, 2, 9]], "k": 7},
            {"mat": [[1, 2], [3, 4], [5, 6], [7, 8]], "k": 16},
            {"mat": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "k": 20},
            {"mat": _rng_sorted_rows(9201, 6, 6, 1, 100), "k": 50},
            {"mat": _rng_sorted_rows(9202, 15, 15, 1, 2000), "k": 150},
            {"mat": _rng_sorted_rows(9203, 30, 30, 1, 5000), "k": 200},
        ],
    },
    # ------------------------------------------------------------------
    # 93. Minimum Area of Three Rectangles Covering All Ones (Hard, 2D Search)
    # ------------------------------------------------------------------
    {
        "slug": "93-minimum-area-three-rectangles-cover-ones",
        "title": "Minimum Area of Three Rectangles Covering All Ones",
        "difficulty": "Hard",
        "subtopic": "2D Search",
        "companies": ["Google", "Meta", "Amazon", "Apple"],
        "desc": (
            "You are given an `m x n` binary matrix `grid` containing at least three `1`s.\n\n"
            "Find **three non-overlapping** axis-aligned rectangles with positive integer area (whose sides lie along grid lines) "
            "such that every `1` in `grid` lies inside at least one of the three rectangles. Return the **minimum possible sum** "
            "of the areas of the three rectangles."
        ),
        "cons": [
            "m == grid.length, n == grid[i].length",
            "1 <= m, n <= 30",
            "grid[i][j] is either 0 or 1.",
            "grid contains at least three 1s.",
        ],
        "hints": [
            "Any three disjoint axis-aligned rectangles can always be separated by guillotine cuts into one of 6 topologies: two horizontal cuts, two vertical cuts, or one T-shaped cut (four orientations).",
            "Build a 2D prefix sum of 1s so you can find the tightest bounding box of all 1s inside any sub-rectangle [r1..r2] x [c1..c2] in O(m + n) time, then evaluate all 6 partition families.",
        ],
        "explanations": [
            "Covering column 0 ((0,0)-(1,0), area 2), cell (1,1) (area 1), and column 2 ((0,2)-(1,2), area 2) yields a minimum total area of 5.",
            "Each of the three isolated 1s at (0,0), (1,2), and (2,1) is covered by its own 1x1 rectangle, giving minimum sum 3.",
            "A 1x4 row [1, 0, 1, 1] splits vertically into [0..0] (area 1), [2..2] (area 1), and [3..3] (area 1), totaling 3.",
        ],
        "time": "O((m^2 + n^2 + m * n) * (m + n))",
        "space": "O(m * n)",
        "method": "minimumSumThreeRectangles",
        "params": [("grid", "int[][]")],
        "ret": "int",
        "py": """        m, n = len(grid), len(grid[0])
        ps = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            row_sum = 0
            for c in range(n):
                row_sum += grid[r][c]
                ps[r + 1][c + 1] = ps[r][c + 1] + row_sum

        INF = 10**9

        def ones(r1: int, r2: int, c1: int, c2: int) -> int:
            return ps[r2 + 1][c2 + 1] - ps[r1][c2 + 1] - ps[r2 + 1][c1] + ps[r1][c1]

        def bbox(r1: int, r2: int, c1: int, c2: int) -> int:
            if ones(r1, r2, c1, c2) == 0:
                return INF
            top = r1
            while ones(top, top, c1, c2) == 0:
                top += 1
            bot = r2
            while ones(bot, bot, c1, c2) == 0:
                bot -= 1
            left = c1
            while ones(top, bot, left, left) == 0:
                left += 1
            right = c2
            while ones(top, bot, right, right) == 0:
                right -= 1
            return (bot - top + 1) * (right - left + 1)

        ans = INF
        # 1. Two horizontal cuts
        for r1 in range(m - 2):
            a1 = bbox(0, r1, 0, n - 1)
            if a1 >= ans:
                continue
            for r2 in range(r1 + 1, m - 1):
                cur = a1 + bbox(r1 + 1, r2, 0, n - 1) + bbox(r2 + 1, m - 1, 0, n - 1)
                if cur < ans:
                    ans = cur
        # 2. Two vertical cuts
        for c1 in range(n - 2):
            a1 = bbox(0, m - 1, 0, c1)
            if a1 >= ans:
                continue
            for c2 in range(c1 + 1, n - 1):
                cur = a1 + bbox(0, m - 1, c1 + 1, c2) + bbox(0, m - 1, c2 + 1, n - 1)
                if cur < ans:
                    ans = cur
        # 3-6. Four T-shaped cuts
        for r in range(m - 1):
            top_full = bbox(0, r, 0, n - 1)
            bot_full = bbox(r + 1, m - 1, 0, n - 1)
            for c in range(n - 1):
                tl = bbox(0, r, 0, c)
                tr = bbox(0, r, c + 1, n - 1)
                bl = bbox(r + 1, m - 1, 0, c)
                br = bbox(r + 1, m - 1, c + 1, n - 1)
                left_full = bbox(0, m - 1, 0, c)
                right_full = bbox(0, m - 1, c + 1, n - 1)
                cand = min(
                    top_full + bl + br,
                    tl + tr + bot_full,
                    left_full + tr + br,
                    tl + bl + right_full,
                )
                if cand < ans:
                    ans = cand
        return ans""",
        "java": """        int m = grid.length, n = grid[0].length;
        int[][] ps = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            int rowSum = 0;
            for (int c = 0; c < n; c++) {
                rowSum += grid[r][c];
                ps[r + 1][c + 1] = ps[r][c + 1] + rowSum;
            }
        }
        int INF = 1_000_000_000;
        int ans = INF;
        for (int r1 = 0; r1 < m - 2; r1++) {
            int a1 = bbox(ps, 0, r1, 0, n - 1, INF);
            if (a1 >= ans) continue;
            for (int r2 = r1 + 1; r2 < m - 1; r2++) {
                int a2 = bbox(ps, r1 + 1, r2, 0, n - 1, INF);
                int a3 = bbox(ps, r2 + 1, m - 1, 0, n - 1, INF);
                if (a2 < INF && a3 < INF) {
                    ans = Math.min(ans, a1 + a2 + a3);
                }
            }
        }
        for (int c1 = 0; c1 < n - 2; c1++) {
            int a1 = bbox(ps, 0, m - 1, 0, c1, INF);
            if (a1 >= ans) continue;
            for (int c2 = c1 + 1; c2 < n - 1; c2++) {
                int a2 = bbox(ps, 0, m - 1, c1 + 1, c2, INF);
                int a3 = bbox(ps, 0, m - 1, c2 + 1, n - 1, INF);
                if (a2 < INF && a3 < INF) {
                    ans = Math.min(ans, a1 + a2 + a3);
                }
            }
        }
        for (int r = 0; r < m - 1; r++) {
            int topFull = bbox(ps, 0, r, 0, n - 1, INF);
            int botFull = bbox(ps, r + 1, m - 1, 0, n - 1, INF);
            for (int c = 0; c < n - 1; c++) {
                int tl = bbox(ps, 0, r, 0, c, INF);
                int tr = bbox(ps, 0, r, c + 1, n - 1, INF);
                int bl = bbox(ps, r + 1, m - 1, 0, c, INF);
                int br = bbox(ps, r + 1, m - 1, c + 1, n - 1, INF);
                int leftFull = bbox(ps, 0, m - 1, 0, c, INF);
                int rightFull = bbox(ps, 0, m - 1, c + 1, n - 1, INF);
                if (topFull < INF && bl < INF && br < INF) ans = Math.min(ans, topFull + bl + br);
                if (tl < INF && tr < INF && botFull < INF) ans = Math.min(ans, tl + tr + botFull);
                if (leftFull < INF && tr < INF && br < INF) ans = Math.min(ans, leftFull + tr + br);
                if (tl < INF && bl < INF && rightFull < INF) ans = Math.min(ans, tl + bl + rightFull);
            }
        }
        return ans;""",
        "java_helpers": """    private int ones(int[][] ps, int r1, int r2, int c1, int c2) {
        return ps[r2 + 1][c2 + 1] - ps[r1][c2 + 1] - ps[r2 + 1][c1] + ps[r1][c1];
    }

    private int bbox(int[][] ps, int r1, int r2, int c1, int c2, int inf) {
        if (ones(ps, r1, r2, c1, c2) == 0) return inf;
        int top = r1;
        while (ones(ps, top, top, c1, c2) == 0) top++;
        int bot = r2;
        while (ones(ps, bot, bot, c1, c2) == 0) bot--;
        int left = c1;
        while (ones(ps, top, bot, left, left) == 0) left++;
        int right = c2;
        while (ones(ps, top, bot, right, right) == 0) right--;
        return (bot - top + 1) * (right - left + 1);
    }""",
        "visible": [
            {"grid": [[1, 0, 1], [1, 1, 1]]},
            {"grid": [[1, 0, 0], [0, 0, 1], [0, 1, 0]]},
            {"grid": [[1, 0, 1, 1]]},
        ],
        "hidden": [
            {"grid": [[1], [0], [1], [1]]},
            {"grid": [[1, 0, 1, 0], [0, 1, 0, 1]]},
            {"grid": [[1, 1], [1, 1]]},
            {"grid": [[0, 0, 1], [0, 1, 0], [1, 0, 0]]},
            {"grid": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]},
            {"grid": [[0, 1, 0, 0, 1], [1, 0, 0, 1, 0], [0, 0, 1, 0, 0], [0, 1, 0, 0, 1]]},
            {"grid": _rng_bin_grid(9301, 8, 8, 0.25)},
            {"grid": _rng_bin_grid(9302, 16, 16, 0.12)},
            {"grid": _rng_bin_grid(9303, 25, 25, 0.15)},
        ],
    },
    # ------------------------------------------------------------------
    # 94. Largest Submatrix With Equal Zeros and Ones (Medium, 2D Search)
    # ------------------------------------------------------------------
    {
        "slug": "94-largest-submatrix-with-equal-zeros-and-ones",
        "title": "Largest Submatrix With Equal Zeros and Ones",
        "difficulty": "Medium",
        "subtopic": "2D Search",
        "companies": ["Amazon", "Microsoft", "Meta", "Goldman Sachs"],
        "desc": (
            "Given an `m x n` binary matrix `grid` consisting of `0`s and `1`s, return the **maximum area** (number of cells) "
            "of a contiguous axis-aligned submatrix that contains an equal number of `0`s and `1`s.\n\n"
            "If no such submatrix exists, return `0`."
        ),
        "cons": [
            "m == grid.length, n == grid[i].length",
            "1 <= m, n <= 120",
            "grid[i][j] is either 0 or 1.",
        ],
        "hints": [
            "Replace every 0 conceptually with -1; then a submatrix has equal counts of 0s and 1s if and only if its sum is 0.",
            "Fix top and bottom rows (r1, r2), compress each column between r1 and r2 into a 1D array of column sums, and find the longest zero-sum subarray in O(n) using a hash map of first-seen prefix sums.",
        ],
        "explanations": [
            "The entire 2x3 matrix has three 0s and three 1s, giving area 6.",
            "No submatrix has equal 0s and 1s because all cells are 1, so the answer is 0.",
            "The largest balanced submatrix has 3 rows and 2 columns (6 cells: three 0s and three 1s).",
        ],
        "time": "O(min(m, n)^2 * max(m, n))",
        "space": "O(max(m, n))",
        "method": "largestEqualZeroOneSubmatrix",
        "params": [("grid", "int[][]")],
        "ret": "int",
        "py": """        m, n = len(grid), len(grid[0])
        if m > n:
            grid = [[grid[r][c] for r in range(m)] for c in range(n)]
            m, n = n, m
        best = 0
        for r1 in range(m):
            col = [0] * n
            for r2 in range(r1, m):
                height = r2 - r1 + 1
                row = grid[r2]
                prefix = 0
                first = {0: -1}
                for c in range(n):
                    col[c] += 1 if row[c] == 1 else -1
                    prefix += col[c]
                    if prefix in first:
                        area = height * (c - first[prefix])
                        if area > best:
                            best = area
                    else:
                        first[prefix] = c
        return best""",
        "java": """        int m = grid.length, n = grid[0].length;
        int[][] g = grid;
        if (m > n) {
            g = new int[n][m];
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) g[c][r] = grid[r][c];
            }
            int tmp = m;
            m = n;
            n = tmp;
        }
        int best = 0;
        int[] col = new int[n];
        for (int r1 = 0; r1 < m; r1++) {
            Arrays.fill(col, 0);
            for (int r2 = r1; r2 < m; r2++) {
                int height = r2 - r1 + 1;
                int[] row = g[r2];
                int prefix = 0;
                Map<Integer, Integer> first = new HashMap<>();
                first.put(0, -1);
                for (int c = 0; c < n; c++) {
                    col[c] += (row[c] == 1) ? 1 : -1;
                    prefix += col[c];
                    Integer prev = first.get(prefix);
                    if (prev != null) {
                        int area = height * (c - prev);
                        if (area > best) best = area;
                    } else {
                        first.put(prefix, c);
                    }
                }
            }
        }
        return best;""",
        "visible": [
            {"grid": [[0, 1, 0], [1, 0, 1]]},
            {"grid": [[1, 1], [1, 1]]},
            {"grid": [[1, 0, 1], [1, 0, 0], [0, 1, 1]]},
        ],
        "hidden": [
            {"grid": [[0]]},
            {"grid": [[0, 1]]},
            {"grid": [[0], [0], [1], [1], [0]]},
            {"grid": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]},
            {"grid": [[1, 0, 0, 1], [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 1, 1]]},
            {"grid": [[0, 0, 1, 0, 0], [0, 1, 0, 0, 0], [0, 0, 0, 0, 0]]},
            {"grid": _rng_bin_grid(9401, 10, 12, 0.45)},
            {"grid": _rng_bin_grid(9402, 24, 6, 0.55)},
            {"grid": _rng_bin_grid(9403, 35, 35, 0.50)},
        ],
    },
    # ------------------------------------------------------------------
    # 95. Surface Area of 3D Shapes on a Grid (Easy, Simulation)
    # ------------------------------------------------------------------
    {
        "slug": "95-surface-area-of-3d-grid-shapes",
        "title": "Surface Area of 3D Shapes on a Grid",
        "difficulty": "Easy",
        "subtopic": "Simulation",
        "companies": ["Amazon", "Apple", "Microsoft"],
        "desc": (
            "You are given an `n x n` integer matrix `grid` where `grid[r][c]` denotes the number of `1 x 1 x 1` cubes "
            "stacked vertically on cell `(r, c)`. Cubes placed on adjacent cells are glued together along their shared faces.\n\n"
            "Return the **total surface area** of all resulting 3D shapes, including the bottom faces resting on the ground."
        ),
        "cons": [
            "n == grid.length == grid[i].length",
            "1 <= n <= 50",
            "0 <= grid[i][j] <= 50",
        ],
        "hints": [
            "An isolated tower of height v > 0 contributes 4 * v side area plus 2 for its top and bottom faces.",
            "Whenever two orthogonally adjacent towers of heights a and b touch, they hide 2 * min(a, b) square units of surface area (one face on each tower); subtract overlaps with the north and west neighbors to avoid double counting.",
        ],
        "explanations": [
            "A single stack of 2 cubes has 4 * 2 + 2 = 10 unit faces.",
            "Four stacks [1,2; 3,4] contribute 6 + 10 + 14 + 18 = 48 minus shared internal faces 2*(1+1+2+3) = 14, giving 34.",
            "Empty cells (height 0) add 0 and the two non-empty diagonal corners share no faces, contributing 6 + 10 = 16.",
        ],
        "time": "O(n^2)",
        "space": "O(1)",
        "method": "surfaceArea",
        "params": [("grid", "int[][]")],
        "ret": "int",
        "py": """        n = len(grid)
        area = 0
        for r in range(n):
            for c in range(n):
                v = grid[r][c]
                if v > 0:
                    area += 4 * v + 2
                    if r > 0:
                        area -= 2 * min(v, grid[r - 1][c])
                    if c > 0:
                        area -= 2 * min(v, grid[r][c - 1])
        return area""",
        "java": """        int n = grid.length;
        int area = 0;
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int v = grid[r][c];
                if (v > 0) {
                    area += 4 * v + 2;
                    if (r > 0) area -= 2 * Math.min(v, grid[r - 1][c]);
                    if (c > 0) area -= 2 * Math.min(v, grid[r][c - 1]);
                }
            }
        }
        return area;""",
        "visible": [
            {"grid": [[2]]},
            {"grid": [[1, 2], [3, 4]]},
            {"grid": [[1, 0], [0, 2]]},
        ],
        "hidden": [
            {"grid": [[0]]},
            {"grid": [[0, 0], [0, 0]]},
            {"grid": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]},
            {"grid": [[2, 2, 2], [2, 1, 2], [2, 2, 2]]},
            {"grid": [[50, 0, 50], [0, 50, 0], [50, 0, 50]]},
            {"grid": [[50] * 5 for _ in range(5)]},
            {"grid": _rng_int_grid(9501, 8, 8, 0, 10)},
            {"grid": _rng_int_grid(9502, 20, 20, 0, 50)},
            {"grid": _rng_int_grid(9503, 40, 40, 0, 50)},
        ],
    },
    # ------------------------------------------------------------------
    # 96. Check Knight Tour Configuration (Medium, Simulation)
    # ------------------------------------------------------------------
    {
        "slug": "96-check-knight-tour-configuration",
        "title": "Check Knight Tour Configuration",
        "difficulty": "Medium",
        "subtopic": "Simulation",
        "companies": ["Amazon", "Google", "Atlassian"],
        "desc": (
            "You are given an `n x n` integer matrix `grid` containing every integer from `0` to `n^2 - 1` exactly once, "
            "where `grid[r][c]` indicates the step index at which a chess knight visits cell `(r, c)`.\n\n"
            "Return `true` if `grid` represents a **valid knight's tour** starting at the top-left corner `(0, 0)` "
            "(meaning `grid[0][0] == 0` and every move from step `t` to `t + 1` is a legal L-shaped knight jump of "
            "2 cells along one axis and 1 cell along the perpendicular axis), and `false` otherwise."
        ),
        "cons": [
            "n == grid.length == grid[i].length",
            "3 <= n <= 30",
            "grid contains every integer in [0, n^2 - 1] exactly once.",
        ],
        "hints": [
            "First verify that the knight actually starts at the top-left corner: grid[0][0] == 0.",
            "From the current position (r, c) at step t, check its at most 8 in-bounds knight neighbors for step t + 1; this verifies the entire tour in O(n^2) time and O(1) extra space.",
        ],
        "explanations": [
            "The 5x5 board starts with 0 at (0, 0) and every consecutive number 0 -> 1 -> ... -> 24 is a valid knight move.",
            "On a 3x3 board, the center cell (1, 1) cannot be reached by a knight from any other cell, so step 7 -> 8 is illegal.",
            "Although consecutive steps form knight jumps, cell (0, 0) is not 0, violating the starting corner requirement.",
        ],
        "time": "O(n^2)",
        "space": "O(1)",
        "method": "checkValidKnightTour",
        "params": [("grid", "int[][]")],
        "ret": "boolean",
        "py": """        n = len(grid)
        if grid[0][0] != 0:
            return False
        moves = ((-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1))
        r, c = 0, 0
        for step in range(1, n * n):
            found = False
            for dr, dc in moves:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == step:
                    r, c = nr, nc
                    found = True
                    break
            if not found:
                return False
        return True""",
        "java": """        int n = grid.length;
        if (grid[0][0] != 0) return false;
        int[][] moves = {{-2, -1}, {-2, 1}, {-1, -2}, {-1, 2}, {1, -2}, {1, 2}, {2, -1}, {2, 1}};
        int r = 0, c = 0;
        for (int step = 1; step < n * n; step++) {
            boolean found = false;
            for (int[] mv : moves) {
                int nr = r + mv[0], nc = c + mv[1];
                if (nr >= 0 && nr < n && nc >= 0 && nc < n && grid[nr][nc] == step) {
                    r = nr;
                    c = nc;
                    found = true;
                    break;
                }
            }
            if (!found) return false;
        }
        return true;""",
        "visible": [
            {
                "grid": [
                    [0, 11, 16, 5, 20],
                    [17, 4, 19, 10, 15],
                    [12, 1, 8, 21, 6],
                    [3, 18, 23, 14, 9],
                    [24, 13, 2, 7, 22],
                ]
            },
            {"grid": [[0, 3, 6], [5, 8, 1], [2, 7, 4]]},
            {
                "grid": [
                    [24, 11, 16, 5, 20],
                    [17, 4, 19, 10, 15],
                    [12, 1, 8, 21, 6],
                    [3, 18, 23, 14, 9],
                    [0, 13, 2, 7, 22],
                ]
            },
        ],
        "hidden": [
            {"grid": _warnsdorff_knight_tour(6)},
            {"grid": _warnsdorff_knight_tour(8)},
            {
                "grid": (
                    lambda g: [row[:] for row in g[:-1]] + [[g[-1][1], g[-1][0]] + g[-1][2:]]
                )(_warnsdorff_knight_tour(6))
            },
            {
                "grid": [
                    [0, 5, 14, 9, 20],
                    [13, 8, 19, 4, 15],
                    [18, 1, 6, 21, 10],
                    [7, 12, 23, 16, 3],
                    [24, 17, 2, 11, 22],
                ]
            },
            {"grid": [[r * 4 + c for c in range(4)] for r in range(4)]},
            {"grid": _warnsdorff_knight_tour(10)},
            {
                "grid": (
                    lambda g: [
                        [g[r][c] if (r, c) not in ((0, 0), (1, 2)) else (1 if (r, c) == (0, 0) else 0) for c in range(8)]
                        for r in range(8)
                    ]
                )(_warnsdorff_knight_tour(8))
            },
            {"grid": _warnsdorff_knight_tour(16)},
            {"grid": _warnsdorff_knight_tour(24)},
        ],
    },
    # ------------------------------------------------------------------
    # 97. Lexicographically Largest Matrix From Row and Column Sums (Medium, Dynamic Grids)
    # ------------------------------------------------------------------
    {
        "slug": "97-restore-matrix-from-row-and-column-sums",
        "title": "Lexicographically Largest Matrix From Row and Column Sums",
        "difficulty": "Medium",
        "subtopic": "Dynamic Grids",
        "companies": ["Google", "Meta", "Amazon", "Uber"],
        "desc": (
            "You are given two non-negative integer arrays `rowSum` of length `m` and `colSum` of length `n` with "
            "`sum(rowSum) == sum(colSum)`.\n\n"
            "Construct an `m x n` matrix of **non-negative integers** whose `i`-th row sums to `rowSum[i]` and whose `j`-th "
            "column sums to `colSum[j]`. Among all valid matrices, return the **lexicographically largest** one when read in "
            "row-major order (comparing cell `(0, 0)` first, then `(0, 1)`, ..., up to `(m - 1, n - 1)`)."
        ),
        "cons": [
            "1 <= rowSum.length, colSum.length <= 200",
            "0 <= rowSum[i], colSum[j] <= 10^8",
            "sum(rowSum) == sum(colSum)",
        ],
        "hints": [
            "To maximize the matrix lexicographically in row-major order, put the largest feasible value min(remRow[r], remCol[c]) into the earliest available cell (r, c).",
            "Each assignment exhausts either row r or column c completely, so you can advance a single pair of pointers (r, c) across the grid in O(m + n) greedy steps.",
        ],
        "explanations": [
            "Cell (0, 0) takes min(3, 4) = 3, exhausting row 0; then row 1 fills column 0 with 1 and column 1 with 7.",
            "Greedily assigning min(remRow[r], remCol[c]) in row-major order places 5 at (0,0), 3 at (1,0), 4 at (1,1), 2 at (2,1), and 8 at (2,2).",
            "When row 0 has sum 0, all of row 0 must be 0, and row 1 absorbs the column sums [2, 0, 5].",
        ],
        "time": "O(m * n)",
        "space": "O(m * n)",
        "method": "restoreMatrix",
        "params": [("rowSum", "int[]"), ("colSum", "int[]")],
        "ret": "int[][]",
        "py": """        m, n = len(rowSum), len(colSum)
        r_rem = rowSum[:]
        c_rem = colSum[:]
        ans = [[0] * n for _ in range(m)]
        r = c = 0
        while r < m and c < n:
            val = r_rem[r] if r_rem[r] < c_rem[c] else c_rem[c]
            ans[r][c] = val
            r_rem[r] -= val
            c_rem[c] -= val
            if r_rem[r] == 0:
                r += 1
            if c_rem[c] == 0:
                c += 1
        return ans""",
        "java": """        int m = rowSum.length, n = colSum.length;
        int[] rRem = Arrays.copyOf(rowSum, m);
        int[] cRem = Arrays.copyOf(colSum, n);
        int[][] ans = new int[m][n];
        int r = 0, c = 0;
        while (r < m && c < n) {
            int val = Math.min(rRem[r], cRem[c]);
            ans[r][c] = val;
            rRem[r] -= val;
            cRem[c] -= val;
            if (rRem[r] == 0) r++;
            if (cRem[c] == 0) c++;
        }
        return ans;""",
        "visible": [
            {"rowSum": [3, 8], "colSum": [4, 7]},
            {"rowSum": [5, 7, 10], "colSum": [8, 6, 8]},
            {"rowSum": [0, 7], "colSum": [2, 0, 5]},
        ],
        "hidden": [
            {"rowSum": [0], "colSum": [0]},
            {"rowSum": [100000000], "colSum": [100000000]},
            {"rowSum": [14, 9], "colSum": [6, 9, 8]},
            {"rowSum": [1, 0, 2, 0], "colSum": [0, 3, 0]},
            {"rowSum": [10, 10, 10], "colSum": [10, 10, 10]},
            {"rowSum": [1, 2, 3, 4, 5], "colSum": [15]},
            {"rowSum": [15], "colSum": [1, 2, 3, 4, 5]},
            _rng_row_col_sums(9701, 10, 12, 500),
            _rng_row_col_sums(9702, 25, 25, 100000),
        ],
    },
    # ------------------------------------------------------------------
    # 98. Minimum Operations to Make a Uni-Value Grid (Medium, Dynamic Grids)
    # ------------------------------------------------------------------
    {
        "slug": "98-minimum-operations-to-make-uni-value-grid",
        "title": "Minimum Operations to Make a Uni-Value Grid",
        "difficulty": "Medium",
        "subtopic": "Dynamic Grids",
        "companies": ["Amazon", "Google", "Bloomberg", "Microsoft"],
        "desc": (
            "You are given an `m x n` integer matrix `grid` and a positive integer `x`. In one operation, you may add `x` "
            "to or subtract `x` from any single element in `grid`.\n\n"
            "Return the **minimum number of operations** required to make all elements in `grid` equal, or `-1` if it is impossible."
        ),
        "cons": [
            "m == grid.length, n == grid[i].length",
            "1 <= m, n <= 200",
            "1 <= grid[i][j], x <= 10^4",
        ],
        "hints": [
            "Adding or subtracting x preserves every element's remainder modulo x, so a solution exists if and only if all elements share the same remainder modulo x.",
            "Once feasibility is verified, flatten and sort all values; moving every element to the median minimizes the total number of x-steps.",
        ],
        "explanations": [
            "All values are congruent mod 2; moving [2, 4, 6, 8] to 4 (or 6) takes 1 + 0 + 1 + 2 = 4 operations.",
            "Moving [1, 5, 2, 3] with x = 1 to median 2 or 3 requires 5 unit steps.",
            "Values 1 and 2 have different remainders modulo 2, so making them equal is impossible (-1).",
        ],
        "time": "O(m * n * log(m * n))",
        "space": "O(m * n)",
        "method": "minOperationsUniValue",
        "params": [("grid", "int[][]"), ("x", "int")],
        "ret": "int",
        "py": """        rem = grid[0][0] % x
        vals = []
        for row in grid:
            for v in row:
                if v % x != rem:
                    return -1
                vals.append(v)
        vals.sort()
        med = vals[len(vals) // 2]
        return sum(abs(v - med) // x for v in vals)""",
        "java": """        int m = grid.length, n = grid[0].length;
        int rem = grid[0][0] % x;
        int[] vals = new int[m * n];
        int idx = 0;
        for (int[] row : grid) {
            for (int v : row) {
                if (v % x != rem) return -1;
                vals[idx++] = v;
            }
        }
        Arrays.sort(vals);
        int med = vals[vals.length / 2];
        int ops = 0;
        for (int v : vals) {
            ops += Math.abs(v - med) / x;
        }
        return ops;""",
        "visible": [
            {"grid": [[2, 4], [6, 8]], "x": 2},
            {"grid": [[1, 5], [2, 3]], "x": 1},
            {"grid": [[1, 2], [3, 4]], "x": 2},
        ],
        "hidden": [
            {"grid": [[7]], "x": 10},
            {"grid": [[5, 5, 5], [5, 5, 5]], "x": 3},
            {"grid": [[1, 10000]], "x": 9999},
            {"grid": [[3, 9, 15, 21, 27]], "x": 3},
            {"grid": [[4], [10], [16], [22]], "x": 6},
            {"grid": [[10, 20, 30], [40, 50, 61]], "x": 10},
            _rng_unival_grid(9801, 10, 10, 7, True),
            _rng_unival_grid(9802, 12, 15, 13, False),
            _rng_unival_grid(9803, 35, 35, 17, True),
        ],
    },
    # ------------------------------------------------------------------
    # 99. Maximum Value Sum by Placing Three Rooks (Hard, Dynamic Grids)
    # ------------------------------------------------------------------
    {
        "slug": "99-maximum-sum-of-three-non-overlapping-rooks",
        "title": "Maximum Value Sum by Placing Three Rooks",
        "difficulty": "Hard",
        "subtopic": "Dynamic Grids",
        "companies": ["Google", "Meta", "Goldman Sachs", "Uber"],
        "desc": (
            "You are given an `m x n` integer matrix `board` representing cell values on a chessboard. You must place "
            "**three rooks** on three cells of `board` such that no two rooks can attack each other (that is, no two rooks "
            "share the same row or the same column).\n\n"
            "Return the **maximum possible sum** of the values of the three cells occupied by the rooks."
        ),
        "cons": [
            "m == board.length, n == board[i].length",
            "3 <= m, n <= 100",
            "-10^9 <= board[i][j] <= 10^9",
        ],
        "hints": [
            "In any single row, you only ever need its top 3 largest values (with their column indices), because the other two rooks can block at most 2 columns.",
            "Fix the middle rook's row r in [1..m-2]; precompute pref[r - 1] (the top 3 distinct-column maximums across rows 0..r-1) and suff[r + 1] (across rows r+1..m-1), then test all 3 x 3 x 3 column-disjoint triples in O(1) per row for O(m * n) total time.",
        ],
        "explanations": [
            "Placing rooks at (0, 2) = 1, (1, 3) = 1, and (2, 1) = 2 uses three distinct rows and columns for a maximum sum of 4.",
            "Placing rooks at (0, 2) = 3, (1, 1) = 5, and (2, 0) = 7 gives 3 + 5 + 7 = 15 (every valid 3-rook placement on this board sums to 15).",
            "All cells equal 1, so any three non-attacking cells sum to 3.",
        ],
        "time": "O(m * n)",
        "space": "O(m)",
        "method": "maximumThreeRooksSum",
        "params": [("board", "int[][]")],
        "ret": "long",
        "py": """        m, n = len(board), len(board[0])

        def row_top3(row):
            top = []
            for c, v in enumerate(row):
                if len(top) < 3 or v > top[-1][0]:
                    top.append((v, c))
                    top.sort(key=lambda x: x[0], reverse=True)
                    if len(top) > 3:
                        top.pop()
            return top

        def merge_top3(a, b):
            best_by_col = {}
            for v, c in a:
                if c not in best_by_col or v > best_by_col[c]:
                    best_by_col[c] = v
            for v, c in b:
                if c not in best_by_col or v > best_by_col[c]:
                    best_by_col[c] = v
            items = sorted(((v, c) for c, v in best_by_col.items()), reverse=True)
            return items[:3]

        rows = [row_top3(board[r]) for r in range(m)]
        pref = [None] * m
        pref[0] = rows[0]
        for r in range(1, m):
            pref[r] = merge_top3(pref[r - 1], rows[r])

        suff = [None] * m
        suff[m - 1] = rows[m - 1]
        for r in range(m - 2, -1, -1):
            suff[r] = merge_top3(suff[r + 1], rows[r])

        ans = -10**18
        for r in range(1, m - 1):
            p_list = pref[r - 1]
            cur_list = rows[r]
            s_list = suff[r + 1]
            for v1, c1 in p_list:
                for v2, c2 in cur_list:
                    if c1 == c2:
                        continue
                    for v3, c3 in s_list:
                        if c3 == c1 or c3 == c2:
                            continue
                        total = v1 + v2 + v3
                        if total > ans:
                            ans = total
        return ans""",
        "java": """        int m = board.length, n = board[0].length;
        int[][][] rows = new int[m][3][2];
        for (int r = 0; r < m; r++) {
            rows[r] = rowTop3(board[r]);
        }
        int[][][] pref = new int[m][][];
        pref[0] = rows[0];
        for (int r = 1; r < m; r++) {
            pref[r] = mergeTop3(pref[r - 1], rows[r]);
        }
        int[][][] suff = new int[m][][];
        suff[m - 1] = rows[m - 1];
        for (int r = m - 2; r >= 0; r--) {
            suff[r] = mergeTop3(suff[r + 1], rows[r]);
        }
        long ans = Long.MIN_VALUE;
        for (int r = 1; r < m - 1; r++) {
            int[][] pList = pref[r - 1];
            int[][] curList = rows[r];
            int[][] sList = suff[r + 1];
            for (int[] p : pList) {
                for (int[] cur : curList) {
                    if (p[1] == cur[1]) continue;
                    for (int[] s : sList) {
                        if (s[1] == p[1] || s[1] == cur[1]) continue;
                        long sum = (long) p[0] + cur[0] + s[0];
                        if (sum > ans) ans = sum;
                    }
                }
            }
        }
        return ans;""",
        "java_helpers": """    private int[][] rowTop3(int[] row) {
        int[][] top = {{Integer.MIN_VALUE, -1}, {Integer.MIN_VALUE, -1}, {Integer.MIN_VALUE, -1}};
        for (int c = 0; c < row.length; c++) {
            int v = row[c];
            if (v > top[0][0]) {
                top[2] = top[1];
                top[1] = top[0];
                top[0] = new int[]{v, c};
            } else if (v > top[1][0]) {
                top[2] = top[1];
                top[1] = new int[]{v, c};
            } else if (v > top[2][0]) {
                top[2] = new int[]{v, c};
            }
        }
        return top;
    }

    private int[][] mergeTop3(int[][] a, int[][] b) {
        int[][] combined = new int[6][2];
        int size = 0;
        for (int[] item : a) {
            size = insertColMax(combined, size, item[0], item[1]);
        }
        for (int[] item : b) {
            size = insertColMax(combined, size, item[0], item[1]);
        }
        Arrays.sort(combined, 0, size, (x, y) -> Integer.compare(y[0], x[0]));
        int[][] res = new int[3][2];
        for (int i = 0; i < 3; i++) {
            res[i] = new int[]{combined[i][0], combined[i][1]};
        }
        return res;
    }

    private int insertColMax(int[][] arr, int size, int v, int c) {
        for (int i = 0; i < size; i++) {
            if (arr[i][1] == c) {
                if (v > arr[i][0]) arr[i][0] = v;
                return size;
            }
        }
        arr[size][0] = v;
        arr[size][1] = c;
        return size + 1;
    }""",
        "visible": [
            {"board": [[-3, 1, 1, 1], [-3, 1, -3, 1], [-3, 2, 1, 1]]},
            {"board": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
            {"board": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]},
        ],
        "hidden": [
            {"board": [[-10, -20, -30], [-40, -50, -60], [-70, -80, -90]]},
            {
                "board": [
                    [1000000000, -1000000000, -1000000000],
                    [-1000000000, 1000000000, -1000000000],
                    [-1000000000, -1000000000, 1000000000],
                ]
            },
            {
                "board": [
                    [-1000000000, -1000000000, -1000000000],
                    [-1000000000, -1000000000, -1000000000],
                    [-1000000000, -1000000000, -1000000000],
                ]
            },
            {"board": [[100, 1, 1], [100, 2, 1], [100, 3, 1], [1, 1, 100]]},
            {"board": [[10, 9, 8, 7, 6], [10, 9, 8, 7, 6], [10, 9, 8, 7, 6]]},
            {"board": _rng_int_grid(9901, 5, 6, -50, 50)},
            {"board": _rng_int_grid(9902, 10, 10, -1000, 1000)},
            {"board": _rng_int_grid(9903, 20, 25, -1000000000, 1000000000)},
            {"board": _rng_int_grid(9904, 35, 35, -1000000000, 1000000000)},
        ],
    },
    # ------------------------------------------------------------------
    # 100. Ways to Cut a Matrix Into K Pieces (Hard, Dynamic Grids)
    # ------------------------------------------------------------------
    {
        "slug": "100-ways-to-cut-matrix-into-k-pieces",
        "title": "Ways to Cut a Matrix Into K Pieces",
        "difficulty": "Hard",
        "subtopic": "Dynamic Grids",
        "companies": ["Google", "Meta", "Amazon", "Netflix"],
        "desc": (
            "You are given an `m x n` grid represented as an array of strings `grid` where `'A'` marks a cell containing an "
            "apple and `'.'` marks an empty cell, along with an integer `k`.\n\n"
            "You need to cut the grid into exactly `k` pieces using `k - 1` sequential cuts. Each cut is either:\n"
            "- **Horizontal**: pick a row split, give away the **top** portion, and keep the remaining **bottom** submatrix.\n"
            "- **Vertical**: pick a column split, give away the **left** portion, and keep the remaining **right** submatrix.\n\n"
            "The final remaining piece is given away as the `k`-th piece. Return the number of valid cutting sequences such "
            "that **every** piece contains at least one `'A'`, modulo `10^9 + 7`."
        ),
        "cons": [
            "1 <= grid.length <= 50",
            "1 <= grid[i].length <= 50",
            "All strings in grid have equal length.",
            "grid[i][j] is either 'A' or '.'.",
            "1 <= k <= 10",
        ],
        "hints": [
            "Because each cut discards either a top strip or a left strip, every remaining submatrix is always a bottom-right suffix [r..m-1] x [c..n-1].",
            "Precompute 2D suffix apple counts apples[r][c], then run bottom-up DP where dp[pieces][r][c] sums dp[pieces - 1][nr][c] over horizontal cuts with apples[r][c] > apples[nr][c] and dp[pieces - 1][r][nc] over vertical cuts with apples[r][c] > apples[r][nc].",
        ],
        "explanations": [
            "With k = 3 on [\"A..\", \"AAA\", \"...\"], there are 3 valid ways to split the grid so each piece has an apple.",
            "With k = 3 on [\"A..\", \"AA.\", \"...\"], there is only 1 valid sequence of two cuts.",
            "With k = 1, no cuts are made and the whole grid already contains an apple, so there is 1 way.",
        ],
        "time": "O(k * m * n * (m + n))",
        "space": "O(m * n)",
        "method": "waysToCutMatrix",
        "params": [("grid", "String[]"), ("k", "int")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007
        m, n = len(grid), len(grid[0])
        apples = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                apples[r][c] = (
                    (1 if grid[r][c] == "A" else 0)
                    + apples[r + 1][c]
                    + apples[r][c + 1]
                    - apples[r + 1][c + 1]
                )
        dp = [[1 if apples[r][c] > 0 else 0 for c in range(n)] for r in range(m)]
        for _ in range(2, k + 1):
            nxt = [[0] * n for _ in range(m)]
            for r in range(m):
                for c in range(n):
                    tot_here = apples[r][c]
                    if tot_here == 0:
                        continue
                    ways = 0
                    for nr in range(r + 1, m):
                        if tot_here - apples[nr][c] > 0:
                            ways += dp[nr][c]
                    for nc in range(c + 1, n):
                        if tot_here - apples[r][nc] > 0:
                            ways += dp[r][nc]
                    nxt[r][c] = ways % MOD
            dp = nxt
        return dp[0][0]""",
        "java": """        int MOD = 1_000_000_007;
        int m = grid.length, n = grid[0].length();
        int[][] apples = new int[m + 1][n + 1];
        for (int r = m - 1; r >= 0; r--) {
            for (int c = n - 1; c >= 0; c--) {
                apples[r][c] = (grid[r].charAt(c) == 'A' ? 1 : 0)
                    + apples[r + 1][c]
                    + apples[r][c + 1]
                    - apples[r + 1][c + 1];
            }
        }
        int[][] dp = new int[m][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                dp[r][c] = apples[r][c] > 0 ? 1 : 0;
            }
        }
        for (int pieces = 2; pieces <= k; pieces++) {
            int[][] nxt = new int[m][n];
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n; c++) {
                    int totHere = apples[r][c];
                    if (totHere == 0) continue;
                    long ways = 0;
                    for (int nr = r + 1; nr < m; nr++) {
                        if (totHere - apples[nr][c] > 0) ways += dp[nr][c];
                    }
                    for (int nc = c + 1; nc < n; nc++) {
                        if (totHere - apples[r][nc] > 0) ways += dp[r][nc];
                    }
                    nxt[r][c] = (int) (ways % MOD);
                }
            }
            dp = nxt;
        }
        return dp[0][0];""",
        "visible": [
            {"grid": ["A..", "AAA", "..."], "k": 3},
            {"grid": ["A..", "AA.", "..."], "k": 3},
            {"grid": ["A..", "A..", "..."], "k": 1},
        ],
        "hidden": [
            {"grid": ["."], "k": 1},
            {"grid": ["A"], "k": 1},
            {"grid": ["A"], "k": 2},
            {"grid": ["AAAA"], "k": 3},
            {"grid": ["A", ".", "A", "A"], "k": 3},
            {"grid": ["...", "...", "..."], "k": 2},
            {"grid": ["AAAA", "AAAA", "AAAA", "AAAA"], "k": 5},
            {"grid": _rng_apple_grid(10001, 12, 12, 0.35), "k": 7},
            {"grid": _rng_apple_grid(10002, 25, 25, 0.50), "k": 10},
        ],
    },
]


def main() -> None:
    expected_prefixes = list(range(84, 101))
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
        assert p["subtopic"] in ALLOWED_SUBTOPICS, f"Invalid subtopic {p['subtopic']} in {p['slug']}"
        for comp in p["companies"]:
            assert comp in ALLOWED_COMPANIES, f"Invalid company {comp} in {p['slug']}"

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

        # Verify no duplicate test inputs
        seen_inputs = set()
        for t in p["visible"] + p["hidden"]:
            key = json.dumps(t, sort_keys=True)
            assert key not in seen_inputs, f"Duplicate test input in {p['slug']}"
            seen_inputs.add(key)

        folder.mkdir(parents=True, exist_ok=True)

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

    print(f"Generated {len(TASKS)} matrix problems (84-100) in {BASE}")


if __name__ == "__main__":
    main()
