#!/usr/bin/env python3
"""Generate matrix problems 24-53 for AlgoPlay (batch 1)."""
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


def _rng_sorted_rows_bin(seed: int, m: int, n: int, ones_first: bool = True) -> list[list[int]]:
    rng = random.Random(seed)
    grid = []
    for _ in range(m):
        cnt = rng.randint(0, n)
        if ones_first:
            grid.append([1] * cnt + [0] * (n - cnt))
        else:
            grid.append([0] * (n - cnt) + [1] * cnt)
    return grid


def _rng_box(seed: int, m: int, n: int) -> list[list[str]]:
    rng = random.Random(seed)
    chars = ["#", "#", ".", ".", ".", "*"]
    return [[rng.choice(chars) for _ in range(n)] for _ in range(m)]


def _rng_ball_grid(seed: int, m: int, n: int) -> list[list[int]]:
    rng = random.Random(seed)
    return [[rng.choice([1, -1]) for _ in range(n)] for _ in range(m)]


def _connected_black_grid(m: int, n: int, r0: int, r1: int, c0: int, c1: int, seed: int) -> tuple[list[list[str]], int, int]:
    """Create a guaranteed single-component '1' region filling bounding box [r0..r1, c0..c1]."""
    rng = random.Random(seed)
    g = [["0"] * n for _ in range(m)]
    # Start with a cross spanning [r0..r1, c0..c1] so the bounding box is exact and connected
    mr = (r0 + r1) // 2
    mc = (c0 + c1) // 2
    for r in range(r0, r1 + 1):
        g[r][mc] = "1"
    for c in range(c0, c1 + 1):
        g[mr][c] = "1"
    # Grow random adjacent cells inside [r0..r1, c0..c1]
    frontier = [(mr, mc)]
    for _ in range((r1 - r0 + 1) * (c1 - c0 + 1) // 2):
        r = rng.randint(r0, r1)
        c = rng.randint(c0, c1)
        if g[r][c] == "0":
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if r0 <= nr <= r1 and c0 <= nc <= c1 and g[nr][nc] == "1":
                    g[r][c] = "1"
                    frontier.append((r, c))
                    break
    return g, mr, mc


def _battleships_grid(seed: int, m: int, n: int, count: int) -> list[list[str]]:
    """Place non-touching horizontal or vertical battleships on an m x n board."""
    rng = random.Random(seed)
    g = [["."] * n for _ in range(m)]
    for _ in range(count * 5):
        if count <= 0:
            break
        horiz = rng.choice([True, False])
        length = rng.randint(1, 4)
        if horiz:
            if length > n:
                continue
            r = rng.randint(0, m - 1)
            c = rng.randint(0, n - length)
            cells = [(r, c + k) for k in range(length)]
        else:
            if length > m:
                continue
            r = rng.randint(0, m - length)
            c = rng.randint(0, n - 1)
            cells = [(r + k, c) for k in range(length)]
        ok = True
        for cr, cc in cells:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = cr + dr, cc + dc
                    if 0 <= nr < m and 0 <= nc < n and g[nr][nc] == "X":
                        ok = False
                        break
                if not ok:
                    break
            if not ok:
                break
        if ok:
            for cr, cc in cells:
                g[cr][cc] = "X"
            count -= 1
    return g


def _rng_minesweeper(seed: int, m: int, n: int, mines: int) -> tuple[list[list[str]], list[int]]:
    rng = random.Random(seed)
    g = [["E"] * n for _ in range(m)]
    coords = [(r, c) for r in range(m) for c in range(n)]
    rng.shuffle(coords)
    for r, c in coords[:mines]:
        g[r][c] = "M"
    # Pick an empty cell away from mines if possible
    for r, c in coords[mines:]:
        has_mine = any(
            0 <= r + dr < m and 0 <= c + dc < n and g[r + dr][c + dc] == "M"
            for dr in (-1, 0, 1)
            for dc in (-1, 0, 1)
        )
        if not has_mine:
            return g, [r, c]
    return g, [coords[-1][0], coords[-1][1]]


def _rng_guards_walls(seed: int, m: int, n: int, num_g: int, num_w: int) -> tuple[list[list[int]], list[list[int]]]:
    rng = random.Random(seed)
    coords = [(r, c) for r in range(m) for c in range(n)]
    rng.shuffle(coords)
    guards = [[r, c] for r, c in coords[:num_g]]
    walls = [[r, c] for r, c in coords[num_g : num_g + num_w]]
    return guards, walls


def _rng_queries(seed: int, n: int, q: int) -> list[list[int]]:
    rng = random.Random(seed)
    out = []
    for _ in range(q):
        r1, r2 = sorted((rng.randint(0, n - 1), rng.randint(0, n - 1)))
        c1, c2 = sorted((rng.randint(0, n - 1), rng.randint(0, n - 1)))
        out.append([r1, c1, r2, c2])
    return out


def _rng_stamp_grid(seed: int, m: int, n: int, h: int, w: int, feasible: bool) -> list[list[int]]:
    rng = random.Random(seed)
    g = [[1] * n for _ in range(m)]
    # Carve out several h x w rectangles of 0s so it's guaranteed stampable
    for _ in range(max(4, (m * n) // (h * w + 1))):
        r = rng.randint(0, m - h)
        c = rng.randint(0, n - w)
        for dr in range(h):
            for dc in range(w):
                g[r + dr][c + dc] = 0
    if not feasible:
        # Isolate a single 0 cell surrounded by 1s (if h > 1 or w > 1)
        for r in range(m):
            for c in range(n):
                g[r][c] = 1
        g[0][0] = 0
        if m >= 3 and n >= 3:
            g[m - 1][n - 1] = 0
    return g


TASKS: list[dict] = []

# ============================================================================
# Subtopic 1: Spiral Traversal (24 - 29)
# ============================================================================

TASKS.append({
    "slug": "24-spiral-matrix-iii",
    "title": "Outward Spiral Matrix Walk",
    "difficulty": "Medium",
    "subtopic": "Spiral Traversal",
    "companies": ["Google", "Amazon", "Meta", "Uber"],
    "desc": (
        "You start at the cell `(rStart, cStart)` of an `rows x cols` grid facing east. "
        "The top-left corner is at `(0, 0)` and the bottom-right corner is at `(rows - 1, cols - 1)`.\n\n"
        "You walk in a clockwise outward spiral to visit every position in this grid. Whenever you step outside "
        "the grid boundary, you continue walking outside and may re-enter the grid later. Specifically, starting at "
        "`(rStart, cStart)`, take 1 step east, 1 step south, 2 steps west, 2 steps north, 3 steps east, 3 steps south, "
        "and so on.\n\n"
        "Return a 2D array of `[r, c]` coordinates representing every cell of the grid in the exact order it is visited."
    ),
    "cons": [
        "1 <= rows, cols <= 100",
        "0 <= rStart < rows",
        "0 <= cStart < cols",
    ],
    "hints": [
        "Notice the step lengths along the directions East, South, West, North follow the sequence 1, 1, 2, 2, 3, 3, 4, 4, ...",
        "Advance step by step along the current direction, recording coordinates whenever 0 <= r < rows and 0 <= c < cols until all rows * cols cells are collected.",
    ],
    "explanations": [
        "Starting at (0, 0) in a 1x4 grid, the walk visits (0, 0) then moves east through (0, 1), (0, 2), and (0, 3).",
        "Starting at (1, 4) in a 5x6 grid, the spiral steps outside the right boundary and re-enters on the south and west legs until all 30 cells are recorded.",
        "A 1x1 grid only contains (0, 0), which is visited immediately.",
    ],
    "time": "O(max(rows, cols)^2)",
    "space": "O(rows * cols)",
    "method": "spiralMatrixIII",
    "params": [("rows", "int"), ("cols", "int"), ("rStart", "int"), ("cStart", "int")],
    "ret": "int[][]",
    "py": """        total = rows * cols
        res = [[rStart, cStart]]
        dirs = ((0, 1), (1, 0), (0, -1), (-1, 0))
        r, c = rStart, cStart
        step = 1
        d = 0
        while len(res) < total:
            for _ in range(2):
                dr, dc = dirs[d]
                for _ in range(step):
                    r += dr
                    c += dc
                    if 0 <= r < rows and 0 <= c < cols:
                        res.append([r, c])
                        if len(res) == total:
                            return res
                d = (d + 1) & 3
            step += 1
        return res""",
    "java": """        int total = rows * cols;
        int[][] res = new int[total][2];
        int idx = 0;
        res[idx][0] = rStart;
        res[idx][1] = cStart;
        idx++;
        int[][] dirs = {{0, 1}, {1, 0}, {0, -1}, {-1, 0}};
        int r = rStart, c = cStart, step = 1, d = 0;
        while (idx < total) {
            for (int rep = 0; rep < 2; rep++) {
                int dr = dirs[d][0], dc = dirs[d][1];
                for (int s = 0; s < step; s++) {
                    r += dr;
                    c += dc;
                    if (r >= 0 && r < rows && c >= 0 && c < cols) {
                        res[idx][0] = r;
                        res[idx][1] = c;
                        idx++;
                        if (idx == total) return res;
                    }
                }
                d = (d + 1) & 3;
            }
            step++;
        }
        return res;""",
    "visible": [
        {"rows": 1, "cols": 4, "rStart": 0, "cStart": 0},
        {"rows": 5, "cols": 6, "rStart": 1, "cStart": 4},
        {"rows": 1, "cols": 1, "rStart": 0, "cStart": 0},
    ],
    "hidden": [
        {"rows": 4, "cols": 1, "rStart": 3, "cStart": 0},
        {"rows": 2, "cols": 2, "rStart": 0, "cStart": 0},
        {"rows": 2, "cols": 2, "rStart": 1, "cStart": 1},
        {"rows": 3, "cols": 3, "rStart": 1, "cStart": 1},
        {"rows": 3, "cols": 3, "rStart": 2, "cStart": 0},
        {"rows": 3, "cols": 5, "rStart": 0, "cStart": 4},
        {"rows": 6, "cols": 4, "rStart": 5, "cStart": 3},
        {"rows": 7, "cols": 7, "rStart": 3, "cStart": 3},
        {"rows": 25, "cols": 30, "rStart": 12, "cStart": 17},
    ],
})

TASKS.append({
    "slug": "25-snake-pattern-matrix-traversal",
    "title": "Snake Pattern Matrix Traversal",
    "difficulty": "Easy",
    "subtopic": "Spiral Traversal",
    "companies": ["Amazon", "Microsoft", "Adobe"],
    "desc": (
        "Given an `m x n` integer `matrix`, return a 1D array of all elements visited in a horizontal snake "
        "(boustrophedon) pattern.\n\n"
        "Traverse rows from top (`row = 0`) to bottom (`row = m - 1`). Even-indexed rows (`0, 2, 4, ...`) are "
        "read from left to right, and odd-indexed rows (`1, 3, 5, ...`) are read from right to left."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 100",
        "-10^5 <= matrix[i][j] <= 10^5",
    ],
    "hints": [
        "Process each row independently from index 0 to m - 1.",
        "Append row elements forward when row % 2 == 0 and in reverse when row % 2 == 1.",
    ],
    "explanations": [
        "Row 0 goes left-to-right [1, 2, 3], row 1 goes right-to-left [6, 5, 4], and row 2 goes left-to-right [7, 8, 9].",
        "Row 0 yields [10, 20] and row 1 reversed yields [40, 30].",
        "A single column visits every row from top to bottom regardless of direction.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "snakeTraverse",
    "params": [("matrix", "int[][]")],
    "ret": "int[]",
    "py": """        res = []
        for r, row in enumerate(matrix):
            if r % 2 == 0:
                res.extend(row)
            else:
                res.extend(reversed(row))
        return res""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        int[] res = new int[m * n];
        int idx = 0;
        for (int r = 0; r < m; r++) {
            if ((r & 1) == 0) {
                for (int c = 0; c < n; c++) res[idx++] = matrix[r][c];
            } else {
                for (int c = n - 1; c >= 0; c--) res[idx++] = matrix[r][c];
            }
        }
        return res;""",
    "visible": [
        {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        {"matrix": [[10, 20], [30, 40]]},
        {"matrix": [[5], [-2], [8], [0]]},
    ],
    "hidden": [
        {"matrix": [[42]]},
        {"matrix": [[1, 2, 3, 4, 5]]},
        {"matrix": [[-1, -2, -3], [-4, -5, -6]]},
        {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]},
        {"matrix": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]},
        {"matrix": [[100000, -100000], [-100000, 100000], [1, 2]]},
        {"matrix": [[9, 8], [7, 6], [5, 4], [3, 2], [1, 0]]},
        {"matrix": _rng_int_grid(2501, 10, 12, -50, 50)},
        {"matrix": _rng_int_grid(2502, 35, 35, -100000, 100000)},
    ],
})

TASKS.append({
    "slug": "26-concentric-ring-sums",
    "title": "Concentric Ring Sums",
    "difficulty": "Easy",
    "subtopic": "Spiral Traversal",
    "companies": ["Google", "Bloomberg", "Oracle"],
    "desc": (
        "Given an `m x n` integer `matrix`, partition its cells into concentric rectangular rings from the outermost "
        "border inward.\n\n"
        "Ring `0` consists of all cells on the outer border of the matrix; ring `1` consists of the outer border "
        "remaining after removing ring `0`, and so on until all cells are accounted for. Note that the innermost "
        "ring may degenerate into a single row, a single column, or a single cell.\n\n"
        "Return an integer array `sums` where `sums[k]` is the sum of all elements in ring `k`."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 100",
        "-10^4 <= matrix[i][j] <= 10^4",
    ],
    "hints": [
        "Maintain four shrinking boundaries: top, bottom, left, and right, just like spiral traversal.",
        "Carefully avoid double-counting corner cells and handle the degenerate cases where top == bottom or left == right.",
    ],
    "explanations": [
        "Outer ring sums 1+2+3+6+9+8+7+4 = 40, and the single center cell forms ring 1 with sum 5.",
        "Ring 0 contains the 10 outer border elements summing to 65; ring 1 is the inner row [6, 7] summing to 13.",
        "A 1x4 matrix has only one ring containing all 4 elements, summing to 10.",
    ],
    "time": "O(m * n)",
    "space": "O(min(m, n))",
    "method": "concentricRingSums",
    "params": [("matrix", "int[][]")],
    "ret": "int[]",
    "py": """        m, n = len(matrix), len(matrix[0])
        top, bottom, left, right = 0, m - 1, 0, n - 1
        res = []
        while top <= bottom and left <= right:
            s = 0
            for c in range(left, right + 1):
                s += matrix[top][c]
            if bottom > top:
                for c in range(left, right + 1):
                    s += matrix[bottom][c]
            for r in range(top + 1, bottom):
                s += matrix[r][left]
                if right > left:
                    s += matrix[r][right]
            res.append(s)
            top += 1
            bottom -= 1
            left += 1
            right -= 1
        return res""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        int rings = (Math.min(m, n) + 1) / 2;
        int[] res = new int[rings];
        int top = 0, bottom = m - 1, left = 0, right = n - 1, idx = 0;
        while (top <= bottom && left <= right) {
            int s = 0;
            for (int c = left; c <= right; c++) s += matrix[top][c];
            if (bottom > top) {
                for (int c = left; c <= right; c++) s += matrix[bottom][c];
            }
            for (int r = top + 1; r < bottom; r++) {
                s += matrix[r][left];
                if (right > left) s += matrix[r][right];
            }
            res[idx++] = s;
            top++;
            bottom--;
            left++;
            right--;
        }
        return res;""",
    "visible": [
        {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        {"matrix": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]]},
        {"matrix": [[1, 2, 3, 4]]},
    ],
    "hidden": [
        {"matrix": [[-7]]},
        {"matrix": [[3], [4], [5], [6]]},
        {"matrix": [[1, 2], [3, 4]]},
        {"matrix": [[1, 1, 1, 1], [1, 2, 2, 1], [1, 2, 2, 1], [1, 1, 1, 1]]},
        {"matrix": [[1, 1, 1, 1, 1], [1, 2, 2, 2, 1], [1, 2, 3, 2, 1], [1, 2, 2, 2, 1], [1, 1, 1, 1, 1]]},
        {"matrix": [[10, -10, 10], [-10, 5, -10], [10, -10, 10]]},
        {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]]},
        {"matrix": _rng_int_grid(2601, 8, 13, -100, 100)},
        {"matrix": _rng_int_grid(2602, 40, 35, -10000, 10000)},
    ],
})

TASKS.append({
    "slug": "27-cyclically-rotating-a-grid",
    "title": "Cyclically Rotating a Grid",
    "difficulty": "Medium",
    "subtopic": "Spiral Traversal",
    "companies": ["Amazon", "Google", "Meta", "Microsoft"],
    "desc": (
        "You are given an `m x n` integer matrix `grid`, where both `m` and `n` are even integers, and a positive "
        "integer `k`.\n\n"
        "The matrix consists of `min(m, n) / 2` concentric rectangular layers. In one cyclic rotation, every element "
        "in every layer moves one position **counter-clockwise** along its own layer (the top edge shifts left, the "
        "left edge shifts down, the bottom edge shifts right, and the right edge shifts up).\n\n"
        "Return the resulting matrix after performing `k` counter-clockwise cyclic rotations."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "2 <= m, n <= 50",
        "Both m and n are even integers.",
        "1 <= grid[i][j] <= 5000",
        "1 <= k <= 10^9",
    ],
    "hints": [
        "Each concentric layer is completely independent and has its own perimeter length L.",
        "Extract each layer in clockwise order into a 1D list; rotating counter-clockwise by k corresponds to shifting that list left by (k % L) positions.",
    ],
    "explanations": [
        "In a 2x2 grid, one counter-clockwise shift moves 40 down, 30 right, 20 up, and 10 left.",
        "The outer layer of length 12 shifts counter-clockwise by 2 and the inner 2x2 layer of length 4 shifts counter-clockwise by 2.",
        "A 2x4 grid has a single layer of length 8; rotating by k = 8 returns the exact original grid.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "rotateGrid",
    "params": [("grid", "int[][]"), ("k", "int")],
    "ret": "int[][]",
    "py": """        m, n = len(grid), len(grid[0])
        res = [row[:] for row in grid]
        layers = min(m, n) // 2
        for layer in range(layers):
            top, bottom = layer, m - 1 - layer
            left, right = layer, n - 1 - layer
            coords = []
            for c in range(left, right):
                coords.append((top, c))
            for r in range(top, bottom):
                coords.append((r, right))
            for c in range(right, left, -1):
                coords.append((bottom, c))
            for r in range(bottom, top, -1):
                coords.append((r, left))
            length = len(coords)
            shift = k % length
            for i, (r, c) in enumerate(coords):
                sr, sc = coords[(i + shift) % length]
                res[r][c] = grid[sr][sc]
        return res""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[][] res = new int[m][n];
        int layers = Math.min(m, n) / 2;
        for (int layer = 0; layer < layers; layer++) {
            int top = layer, bottom = m - 1 - layer;
            int left = layer, right = n - 1 - layer;
            int len = 2 * ((bottom - top) + (right - left));
            int[] rs = new int[len];
            int[] cs = new int[len];
            int idx = 0;
            for (int c = left; c < right; c++) { rs[idx] = top; cs[idx++] = c; }
            for (int r = top; r < bottom; r++) { rs[idx] = r; cs[idx++] = right; }
            for (int c = right; c > left; c--) { rs[idx] = bottom; cs[idx++] = c; }
            for (int r = bottom; r > top; r--) { rs[idx] = r; cs[idx++] = left; }
            int shift = k % len;
            for (int i = 0; i < len; i++) {
                int src = (i + shift) % len;
                res[rs[i]][cs[i]] = grid[rs[src]][cs[src]];
            }
        }
        return res;""",
    "visible": [
        {"grid": [[40, 10], [30, 20]], "k": 1},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], "k": 2},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8]], "k": 8},
    ],
    "hidden": [
        {"grid": [[1, 2], [3, 4]], "k": 1000000000},
        {"grid": [[1, 2], [3, 4]], "k": 999999999},
        {"grid": [[1, 2], [3, 4], [5, 6], [7, 8]], "k": 3},
        {"grid": [[1, 2, 3, 4, 5, 6], [7, 8, 9, 10, 11, 12]], "k": 5},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], "k": 12},
        {"grid": [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], "k": 13},
        {"grid": _rng_int_grid(2701, 6, 4, 1, 100), "k": 17},
        {"grid": _rng_int_grid(2702, 8, 10, 1, 5000), "k": 123456789},
        {"grid": _rng_int_grid(2703, 30, 32, 1, 5000), "k": 987654321},
    ],
})

TASKS.append({
    "slug": "28-kth-cell-in-spiral-order",
    "title": "Kth Cell in Spiral Order",
    "difficulty": "Hard",
    "subtopic": "Spiral Traversal",
    "companies": ["Google", "Meta", "Goldman Sachs", "Apple"],
    "desc": (
        "Consider a `rows x cols` grid (0-indexed) traversed in standard clockwise spiral order starting at `(0, 0)`: "
        "moving right along the top row, down the rightmost column, left along the bottom row, and up the leftmost "
        "column, peeling layers inward until every cell is visited.\n\n"
        "Given `rows`, `cols`, and a 1-indexed integer `k`, return the 0-indexed coordinates `[r, c]` of the `k`-th "
        "cell visited in this clockwise spiral traversal. Because `rows` and `cols` can be as large as `10^9`, "
        "you cannot construct the grid or simulate cell-by-cell."
    ),
    "cons": [
        "1 <= rows, cols <= 10^9",
        "1 <= k <= rows * cols",
    ],
    "hints": [
        "Peeling the first L complete concentric rings consumes rows * cols - (rows - 2L) * (cols - 2L) cells.",
        "Binary search for the largest ring index L whose preceding rings contain strictly fewer than k cells, then locate the exact side (top, right, bottom, or left) of ring L in O(1) time.",
    ],
    "explanations": [
        "In a 3x3 grid, the clockwise spiral visits (0,0), (0,1), (0,2), (1,2), (2,2), (2,1), (2,0), (1,0), (1,1); the 5th cell is (2, 2).",
        "In a 3x4 grid, the outer ring has 10 cells, so the 11th cell is the start of the inner row at (1, 1).",
        "The 1st cell visited in any grid is always the top-left corner (0, 0).",
    ],
    "time": "O(log(min(rows, cols)))",
    "space": "O(1)",
    "method": "kthSpiralCell",
    "params": [("rows", "int"), ("cols", "int"), ("k", "long")],
    "ret": "int[]",
    "py": """        lo, hi = 0, (min(rows, cols) - 1) // 2
        total = rows * cols
        while lo < hi:
            mid = (lo + hi + 1) // 2
            consumed = total - (rows - 2 * mid) * (cols - 2 * mid)
            if consumed < k:
                lo = mid
            else:
                hi = mid - 1
        layer = lo
        consumed = total - (rows - 2 * layer) * (cols - 2 * layer)
        rem = k - 1 - consumed
        top, bottom = layer, rows - 1 - layer
        left, right = layer, cols - 1 - layer
        w = right - left + 1
        h = bottom - top + 1
        if rem < w:
            return [top, left + rem]
        rem -= w
        if rem < h - 1:
            return [top + 1 + rem, right]
        rem -= h - 1
        if rem < w - 1:
            return [bottom, right - 1 - rem]
        rem -= w - 1
        return [bottom - 1 - rem, left]""",
    "java": """        long R = rows, C = cols;
        long total = R * C;
        long lo = 0, hi = (Math.min(R, C) - 1) / 2;
        while (lo < hi) {
            long mid = (lo + hi + 1) / 2;
            long consumed = total - (R - 2 * mid) * (C - 2 * mid);
            if (consumed < k) lo = mid;
            else hi = mid - 1;
        }
        long layer = lo;
        long consumed = total - (R - 2 * layer) * (C - 2 * layer);
        long rem = k - 1 - consumed;
        long top = layer, bottom = R - 1 - layer;
        long left = layer, right = C - 1 - layer;
        long w = right - left + 1;
        long h = bottom - top + 1;
        if (rem < w) return new int[]{(int) top, (int) (left + rem)};
        rem -= w;
        if (rem < h - 1) return new int[]{(int) (top + 1 + rem), (int) right};
        rem -= (h - 1);
        if (rem < w - 1) return new int[]{(int) bottom, (int) (right - 1 - rem)};
        rem -= (w - 1);
        return new int[]{(int) (bottom - 1 - rem), (int) left};""",
    "visible": [
        {"rows": 3, "cols": 3, "k": 5},
        {"rows": 3, "cols": 4, "k": 11},
        {"rows": 5, "cols": 2, "k": 1},
    ],
    "hidden": [
        {"rows": 1, "cols": 1, "k": 1},
        {"rows": 1, "cols": 1000000000, "k": 765432109},
        {"rows": 1000000000, "cols": 1, "k": 987654321},
        {"rows": 4, "cols": 4, "k": 16},
        {"rows": 4, "cols": 4, "k": 12},
        {"rows": 5, "cols": 7, "k": 35},
        {"rows": 7, "cols": 5, "k": 34},
        {"rows": 1000000000, "cols": 1000000000, "k": 1000000000000000000},
        {"rows": 999999999, "cols": 1000000000, "k": 500000000123456789},
    ],
})

TASKS.append({
    "slug": "29-sort-matrix-diagonally",
    "title": "Sort the Matrix Diagonally",
    "difficulty": "Medium",
    "subtopic": "Spiral Traversal",
    "companies": ["Google", "Amazon", "Apple", "Netflix"],
    "desc": (
        "A matrix diagonal is a line of cells running from top-left toward bottom-right: starting at some cell "
        "`(r, c)` on the top row or leftmost column, and stepping repeatedly to `(r + 1, c + 1)` until reaching "
        "the matrix boundary.\n\n"
        "Given an `m x n` integer matrix `mat`, sort each diagonal in ascending order from top-left to bottom-right "
        "and return the resulting matrix."
    ),
    "cons": [
        "m == mat.length",
        "n == mat[i].length",
        "1 <= m, n <= 100",
        "1 <= mat[i][j] <= 10^4",
    ],
    "hints": [
        "All cells on the same top-left to bottom-right diagonal share the exact same key (r - c).",
        "Collect the elements of each diagonal (either via a map keyed by r - c or by iterating from each border start), sort them, and write them back along the same diagonal.",
    ],
    "explanations": [
        "Sorting each of the 6 diagonals independently yields [[1,1,1,1],[1,2,2,2],[1,2,3,3]].",
        "The main diagonal [5, 1] becomes [1, 5] while single-element diagonals stay unchanged.",
        "A 1x4 matrix has four diagonals of length 1, so it remains unchanged.",
    ],
    "time": "O(m * n * log(min(m, n)))",
    "space": "O(min(m, n))",
    "method": "diagonalSort",
    "params": [("mat", "int[][]")],
    "ret": "int[][]",
    "py": """        m, n = len(mat), len(mat[0])
        res = [row[:] for row in mat]
        starts = [(r, 0) for r in range(m)] + [(0, c) for c in range(1, n)]
        for sr, sc in starts:
            vals = []
            r, c = sr, sc
            while r < m and c < n:
                vals.append(res[r][c])
                r += 1
                c += 1
            vals.sort()
            r, c = sr, sc
            for v in vals:
                res[r][c] = v
                r += 1
                c += 1
        return res""",
    "java": """        int m = mat.length, n = mat[0].length;
        int[][] res = new int[m][n];
        for (int r = 0; r < m; r++) res[r] = mat[r].clone();
        int maxLen = Math.min(m, n);
        int[] buf = new int[maxLen];
        for (int sr = 0; sr < m; sr++) {
            int len = 0, r = sr, c = 0;
            while (r < m && c < n) buf[len++] = res[r++][c++];
            Arrays.sort(buf, 0, len);
            r = sr; c = 0;
            for (int i = 0; i < len; i++) res[r++][c++] = buf[i];
        }
        for (int sc = 1; sc < n; sc++) {
            int len = 0, r = 0, c = sc;
            while (r < m && c < n) buf[len++] = res[r++][c++];
            Arrays.sort(buf, 0, len);
            r = 0; c = sc;
            for (int i = 0; i < len; i++) res[r++][c++] = buf[i];
        }
        return res;""",
    "visible": [
        {"mat": [[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]]},
        {"mat": [[5, 3], [2, 1]]},
        {"mat": [[9, 4, 7, 2]]},
    ],
    "hidden": [
        {"mat": [[42]]},
        {"mat": [[5], [3], [1], [4]]},
        {"mat": [[11, 25, 66, 1, 69, 7], [23, 55, 17, 45, 15, 52], [75, 31, 36, 44, 58, 8], [22, 27, 33, 25, 68, 4], [84, 28, 14, 11, 5, 50]]},
        {"mat": [[9, 8, 7], [6, 5, 4], [3, 2, 1]]},
        {"mat": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
        {"mat": [[7, 7, 7], [7, 7, 7]]},
        {"mat": [[10, 2, 8], [4, 9, 1], [7, 3, 6], [5, 12, 11]]},
        {"mat": _rng_int_grid(2901, 12, 15, 1, 100)},
        {"mat": _rng_int_grid(2902, 35, 35, 1, 10000)},
    ],
})

# ============================================================================
# Subtopic 2: Matrix Rotation (30 - 35)
# ============================================================================

TASKS.append({
    "slug": "30-determine-matrix-obtained-by-rotation",
    "title": "Matrix Obtained By Rotation",
    "difficulty": "Easy",
    "subtopic": "Matrix Rotation",
    "companies": ["Amazon", "Google", "Apple"],
    "desc": (
        "Given two `n x n` integer matrices `mat` and `target`, return `true` if it is possible to make `mat` "
        "identical to `target` by rotating `mat` in 90-degree clockwise increments (0, 90, 180, or 270 degrees), "
        "or `false` otherwise."
    ),
    "cons": [
        "n == mat.length == target.length",
        "n == mat[i].length == target[i].length",
        "1 <= n <= 50",
        "0 <= mat[i][j], target[i][j] <= 100",
    ],
    "hints": [
        "There are only 4 distinct orientations obtained by rotating 90 degrees clockwise: 0, 90, 180, and 270 degrees.",
        "You can check all 4 orientations directly in a single pass using index mappings without allocating rotated copies.",
    ],
    "explanations": [
        "Rotating mat 90 degrees clockwise once matches target.",
        "None of the four 90-degree rotations of mat equals target.",
        "Rotating mat 180 degrees (twice by 90 degrees) matches target.",
    ],
    "time": "O(n^2)",
    "space": "O(1)",
    "method": "findRotation",
    "params": [("mat", "int[][]"), ("target", "int[][]")],
    "ret": "boolean",
    "py": """        n = len(mat)
        ok0 = ok90 = ok180 = ok270 = True
        for r in range(n):
            for c in range(n):
                v = mat[r][c]
                if v != target[r][c]:
                    ok0 = False
                if v != target[c][n - 1 - r]:
                    ok90 = False
                if v != target[n - 1 - r][n - 1 - c]:
                    ok180 = False
                if v != target[n - 1 - c][r]:
                    ok270 = False
        return ok0 or ok90 or ok180 or ok270""",
    "java": """        int n = mat.length;
        boolean ok0 = true, ok90 = true, ok180 = true, ok270 = true;
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int v = mat[r][c];
                if (v != target[r][c]) ok0 = false;
                if (v != target[c][n - 1 - r]) ok90 = false;
                if (v != target[n - 1 - r][n - 1 - c]) ok180 = false;
                if (v != target[n - 1 - c][r]) ok270 = false;
            }
        }
        return ok0 || ok90 || ok180 || ok270;""",
    "visible": [
        {"mat": [[0, 1], [1, 0]], "target": [[1, 0], [0, 1]]},
        {"mat": [[0, 1], [1, 1]], "target": [[1, 0], [0, 1]]},
        {"mat": [[0, 0, 0], [0, 1, 0], [1, 1, 1]], "target": [[1, 1, 1], [0, 1, 0], [0, 0, 0]]},
    ],
    "hidden": [
        {"mat": [[1]], "target": [[1]]},
        {"mat": [[1]], "target": [[0]]},
        {"mat": [[1, 2], [3, 4]], "target": [[1, 2], [3, 4]]},
        {"mat": [[1, 2], [3, 4]], "target": [[2, 4], [1, 3]]},
        {"mat": [[1, 2], [3, 4]], "target": [[2, 1], [4, 3]]},
        {"mat": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "target": [[3, 6, 9], [2, 5, 8], [1, 4, 7]]},
        {"mat": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "target": [[1, 4, 7], [2, 5, 8], [3, 6, 9]]},
        {
            "mat": (g30 := _rng_int_grid(3001, 25, 25, 0, 50)),
            "target": [[g30[24 - c][r] for c in range(25)] for r in range(25)],
        },
        {
            "mat": (g30b := _rng_int_grid(3002, 30, 30, 0, 50)),
            "target": [
                [g30b[29 - r][29 - c] if (r, c) != (15, 15) else (g30b[14][14] ^ 1) for c in range(30)]
                for r in range(30)
            ],
        },
    ],
})

TASKS.append({
    "slug": "31-flip-and-invert-binary-image",
    "title": "Flip and Invert Binary Image",
    "difficulty": "Easy",
    "subtopic": "Matrix Rotation",
    "companies": ["Google", "Apple", "Microsoft"],
    "desc": (
        "Given an `n x n` binary matrix `image` containing only `0`s and `1`s, perform two transformations in order:\n"
        "1. **Flip horizontally**: reverse every row from left to right.\n"
        "2. **Invert**: replace every `0` with `1` and every `1` with `0`.\n\n"
        "Return the resulting binary matrix."
    ),
    "cons": [
        "n == image.length == image[i].length",
        "1 <= n <= 100",
        "image[i][j] is either 0 or 1.",
    ],
    "hints": [
        "Both horizontal reversal and bit inversion can be combined in a single pass per row using two pointers.",
        "For symmetric positions c and n - 1 - c, if image[r][c] != image[r][n - 1 - c] they remain unchanged after reversing and inverting; if they are equal, both bits flip.",
    ],
    "explanations": [
        "Reversing each row gives [[0,1,1],[1,0,1],[0,0,0]], then inverting bits gives [[1,0,0],[0,1,0],[1,1,1]].",
        "Reversing and inverting each of the 4 rows yields the resulting 4x4 matrix.",
        "A single cell [0] flips to itself and inverts to [1].",
    ],
    "time": "O(n^2)",
    "space": "O(n^2)",
    "method": "flipAndInvertImage",
    "params": [("image", "int[][]")],
    "ret": "int[][]",
    "py": """        n = len(image)
        return [[1 - image[r][n - 1 - c] for c in range(n)] for r in range(n)]""",
    "java": """        int n = image.length;
        int[][] res = new int[n][n];
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                res[r][c] = 1 - image[r][n - 1 - c];
            }
        }
        return res;""",
    "visible": [
        {"image": [[1, 1, 0], [1, 0, 1], [0, 0, 0]]},
        {"image": [[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]]},
        {"image": [[0]]},
    ],
    "hidden": [
        {"image": [[1]]},
        {"image": [[0, 0], [0, 0]]},
        {"image": [[1, 1], [1, 1]]},
        {"image": [[1, 0], [0, 1]]},
        {"image": [[0, 1], [1, 0]]},
        {"image": [[1, 0, 1], [0, 1, 0], [1, 0, 1]]},
        {"image": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]},
        {"image": _rng_bin_grid(3101, 15, 15, 0.4)},
        {"image": _rng_bin_grid(3102, 40, 40, 0.55)},
    ],
})

TASKS.append({
    "slug": "32-rotate-rectangular-matrix-clockwise",
    "title": "Rotate Rectangular Matrix Clockwise",
    "difficulty": "Easy",
    "subtopic": "Matrix Rotation",
    "companies": ["Amazon", "Microsoft", "Salesforce", "Atlassian"],
    "desc": (
        "Given a rectangular `m x n` integer `matrix` (where `m` and `n` need not be equal) and a non-negative "
        "integer `rotations`, return the matrix obtained by rotating `matrix` by 90 degrees clockwise `rotations` "
        "times.\n\n"
        "Note that each 90-degree rotation swaps the row and column dimensions: an `m x n` matrix becomes `n x m` "
        "after 1 or 3 rotations, and stays `m x n` after 0 or 2 rotations."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 100",
        "0 <= rotations <= 10^9",
        "-10^4 <= matrix[i][j] <= 10^4",
    ],
    "hints": [
        "Four 90-degree rotations return the matrix to its original state, so only k = rotations % 4 matters.",
        "Map each source cell (r, c) directly to its destination coordinates based on k in {0, 1, 2, 3}.",
    ],
    "explanations": [
        "Rotating a 2x3 matrix once clockwise produces a 3x2 matrix [[4,1],[5,2],[6,3]].",
        "Rotating a 2x3 matrix twice clockwise flips it 180 degrees to [[6,5,4],[3,2,1]].",
        "Rotating 3 times clockwise is equivalent to 90 degrees counter-clockwise, yielding [[3,6],[2,5],[1,4]].",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "rotateMatrix",
    "params": [("matrix", "int[][]"), ("rotations", "int")],
    "ret": "int[][]",
    "py": """        m, n = len(matrix), len(matrix[0])
        k = rotations % 4
        if k == 0:
            return [row[:] for row in matrix]
        if k == 1:
            return [[matrix[m - 1 - r][c] for r in range(m)] for c in range(n)]
        if k == 2:
            return [[matrix[m - 1 - r][n - 1 - c] for c in range(n)] for r in range(m)]
        return [[matrix[r][n - 1 - c] for r in range(m)] for c in range(n)]""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        int k = rotations % 4;
        if (k == 0) {
            int[][] res = new int[m][n];
            for (int r = 0; r < m; r++) res[r] = matrix[r].clone();
            return res;
        }
        if (k == 1) {
            int[][] res = new int[n][m];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    res[c][m - 1 - r] = matrix[r][c];
            return res;
        }
        if (k == 2) {
            int[][] res = new int[m][n];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    res[m - 1 - r][n - 1 - c] = matrix[r][c];
            return res;
        }
        int[][] res = new int[n][m];
        for (int r = 0; r < m; r++)
            for (int c = 0; c < n; c++)
                res[n - 1 - c][r] = matrix[r][c];
        return res;""",
    "visible": [
        {"matrix": [[1, 2, 3], [4, 5, 6]], "rotations": 1},
        {"matrix": [[1, 2, 3], [4, 5, 6]], "rotations": 2},
        {"matrix": [[1, 2, 3], [4, 5, 6]], "rotations": 3},
    ],
    "hidden": [
        {"matrix": [[1, 2, 3], [4, 5, 6]], "rotations": 0},
        {"matrix": [[1, 2, 3], [4, 5, 6]], "rotations": 4},
        {"matrix": [[7]], "rotations": 999999999},
        {"matrix": [[1, 2, 3, 4]], "rotations": 1},
        {"matrix": [[1], [2], [3], [4]], "rotations": 3},
        {"matrix": [[-1, 0, 5], [2, -3, 4], [8, 9, -2]], "rotations": 1000000000},
        {"matrix": [[1, 2], [3, 4], [5, 6], [7, 8]], "rotations": 7},
        {"matrix": _rng_int_grid(3201, 15, 25, -100, 100), "rotations": 123456789},
        {"matrix": _rng_int_grid(3202, 35, 28, -10000, 10000), "rotations": 987654323},
    ],
})

TASKS.append({
    "slug": "33-rotating-the-box",
    "title": "Rotating the Box",
    "difficulty": "Medium",
    "subtopic": "Matrix Rotation",
    "companies": ["Uber", "Amazon", "Google", "Meta"],
    "desc": (
        "You are given an `m x n` character matrix `box` representing a side-view of a box. Each cell is one of:\n"
        "- `'#'`: a stone\n"
        "- `'*'`: a stationary obstacle\n"
        "- `'.'`: an empty space\n\n"
        "The box is rotated **90 degrees clockwise**, causing some of the stones to fall down under gravity until "
        "each stone lands on an obstacle, another stone, or the bottom of the box. Obstacles do not move.\n\n"
        "Return an `n x m` character matrix representing the box after rotation and gravity settle."
    ),
    "cons": [
        "m == box.length",
        "n == box[i].length",
        "1 <= m, n <= 100",
        "box[i][j] is either '#', '*', or '.'.",
    ],
    "hints": [
        "When the box rotates 90 degrees clockwise, moving right along a row becomes moving downward along a column.",
        "Process each row from right to left keeping a write pointer for the lowest available empty slot, resetting it just left of every obstacle '*', and write directly into the rotated n x m output.",
    ],
    "explanations": [
        "Rotating 90 degrees clockwise turns the 1x3 row into a 3x1 column; the top stone falls onto the bottom stone.",
        "The obstacle in row 0 stops the stone above it, while the stones in row 1 settle to the bottom of the rotated column.",
        "Every stone falls down within its obstacle-bounded segment after the 90-degree clockwise turn.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "rotateTheBox",
    "params": [("box", "char[][]")],
    "ret": "char[][]",
    "py": """        m, n = len(box), len(box[0])
        res = [['.'] * m for _ in range(n)]
        for r in range(m):
            dest_col = m - 1 - r
            write = n - 1
            for c in range(n - 1, -1, -1):
                ch = box[r][c]
                if ch == '*':
                    res[c][dest_col] = '*'
                    write = c - 1
                elif ch == '#':
                    res[write][dest_col] = '#'
                    write -= 1
        return res""",
    "java": """        int m = box.length, n = box[0].length;
        char[][] res = new char[n][m];
        for (int i = 0; i < n; i++) Arrays.fill(res[i], '.');
        for (int r = 0; r < m; r++) {
            int destCol = m - 1 - r;
            int write = n - 1;
            for (int c = n - 1; c >= 0; c--) {
                char ch = box[r][c];
                if (ch == '*') {
                    res[c][destCol] = '*';
                    write = c - 1;
                } else if (ch == '#') {
                    res[write][destCol] = '#';
                    write--;
                }
            }
        }
        return res;""",
    "visible": [
        {"box": _grid_from_rows(["#.#"])},
        {"box": _grid_from_rows(["#.*.", "##*."])},
        {"box": _grid_from_rows(["##*.*.", "###*..", "###.#."])},
    ],
    "hidden": [
        {"box": _grid_from_rows(["."])},
        {"box": _grid_from_rows(["#"])},
        {"box": _grid_from_rows(["*"])},
        {"box": _grid_from_rows(["####", "....", "****"])},
        {"box": _grid_from_rows(["#...#", ".#.#.", "..#.."])},
        {"box": _grid_from_rows(["*#*#*#", "#*#*#*"])},
        {"box": _grid_from_rows(["#", ".", "#", "*", ".", "#"])},
        {"box": _rng_box(3301, 12, 16)},
        {"box": _rng_box(3302, 35, 35)},
    ],
})

TASKS.append({
    "slug": "34-image-overlap-translation",
    "title": "Maximum Image Overlap",
    "difficulty": "Medium",
    "subtopic": "Matrix Rotation",
    "companies": ["Google", "Meta", "Apple"],
    "desc": (
        "You are given two `n x n` binary matrices `img1` and `img2` containing only `0`s and `1`s.\n\n"
        "We can translate `img1` by any integer shift `(dr, dc)` (moving it up, down, left, or right without "
        "rotation or wrap-around; any cells shifted outside the `n x n` bounds are discarded). The overlap of a "
        "translation is the number of cells where both the shifted `img1` and `img2` have a `1`.\n\n"
        "Return the largest possible overlap over all integer translations."
    ),
    "cons": [
        "n == img1.length == img1[i].length",
        "n == img2.length == img2[i].length",
        "1 <= n <= 30",
        "img1[i][j] and img2[i][j] are either 0 or 1.",
    ],
    "hints": [
        "Collect the coordinates of all 1-cells in img1 and all 1-cells in img2.",
        "Every pair (p1, p2) of 1-cells agrees under the unique translation vector (p2.r - p1.r, p2.c - p1.c); count the most frequent vector.",
    ],
    "explanations": [
        "Translating img1 right by 1 and down by 1 aligns three 1-cells with img2.",
        "With a 1x1 matrix of [1] and [1], zero translation gives overlap 1.",
        "Because img1 has no 1-cells, no translation can produce any overlap.",
    ],
    "time": "O(n^4)",
    "space": "O(n^2)",
    "method": "largestOverlap",
    "params": [("img1", "int[][]"), ("img2", "int[][]")],
    "ret": "int",
    "py": """        n = len(img1)
        ones1 = [(r, c) for r in range(n) for c in range(n) if img1[r][c] == 1]
        ones2 = [(r, c) for r in range(n) for c in range(n) if img2[r][c] == 1]
        if not ones1 or not ones2:
            return 0
        counts = {}
        best = 0
        for r1, c1 in ones1:
            for r2, c2 in ones2:
                key = (r2 - r1, c2 - c1)
                val = counts.get(key, 0) + 1
                counts[key] = val
                if val > best:
                    best = val
        return best""",
    "java": """        int n = img1.length;
        List<int[]> ones1 = new ArrayList<>();
        List<int[]> ones2 = new ArrayList<>();
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                if (img1[r][c] == 1) ones1.add(new int[]{r, c});
                if (img2[r][c] == 1) ones2.add(new int[]{r, c});
            }
        }
        int span = 2 * n;
        int[][] counts = new int[span][span];
        int best = 0;
        for (int[] p1 : ones1) {
            for (int[] p2 : ones2) {
                int dr = p2[0] - p1[0] + n;
                int dc = p2[1] - p1[1] + n;
                int val = ++counts[dr][dc];
                if (val > best) best = val;
            }
        }
        return best;""",
    "visible": [
        {"img1": [[1, 1, 0], [0, 1, 0], [0, 1, 0]], "img2": [[0, 0, 0], [0, 1, 1], [0, 0, 1]]},
        {"img1": [[1]], "img2": [[1]]},
        {"img1": [[0]], "img2": [[1]]},
    ],
    "hidden": [
        {"img1": [[0, 0], [0, 0]], "img2": [[0, 0], [0, 0]]},
        {"img1": [[1, 1], [1, 1]], "img2": [[1, 1], [1, 1]]},
        {"img1": [[1, 0], [0, 0]], "img2": [[0, 0], [0, 1]]},
        {"img1": [[0, 0, 1], [0, 1, 0], [1, 0, 0]], "img2": [[1, 0, 0], [0, 1, 0], [0, 0, 1]]},
        {"img1": [[1, 0, 1], [0, 1, 0], [1, 0, 1]], "img2": [[0, 1, 0], [1, 0, 1], [0, 1, 0]]},
        {"img1": [[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], "img2": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 1]]},
        {"img1": _rng_bin_grid(3401, 8, 8, 0.35), "img2": _rng_bin_grid(3402, 8, 8, 0.35)},
        {"img1": _rng_bin_grid(3403, 18, 18, 0.4), "img2": _rng_bin_grid(3404, 18, 18, 0.4)},
        {"img1": _rng_bin_grid(3405, 28, 28, 0.45), "img2": _rng_bin_grid(3406, 28, 28, 0.45)},
    ],
})

TASKS.append({
    "slug": "35-minimum-flips-for-palindromic-grid",
    "title": "Minimum Flips for Palindromic Grid",
    "difficulty": "Medium",
    "subtopic": "Matrix Rotation",
    "companies": ["Amazon", "Google", "LinkedIn"],
    "desc": (
        "You are given an `m x n` binary matrix `grid` containing only `0`s and `1`s.\n\n"
        "A row or column is considered **palindromic** if its values read the same forward and backward. "
        "In a single operation, you may flip any cell (`0` to `1`, or `1` to `0`).\n\n"
        "Return the minimum number of flips required so that **either** all rows are palindromic **or** all "
        "columns are palindromic."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 200",
        "grid[i][j] is either 0 or 1.",
    ],
    "hints": [
        "Making all rows palindromic and making all columns palindromic are independent goals; compute both costs and take the minimum.",
        "To make a row palindromic, count symmetric pairs (c, n - 1 - c) that differ—each differing pair requires exactly 1 flip.",
    ],
    "explanations": [
        "Flipping two cells makes all rows palindromic, whereas making all columns palindromic requires 3 flips; the minimum is 2.",
        "Flipping just cell (2, 1) makes both columns palindromic in 1 flip, while rows need 2 flips.",
        "Every single-element row (and column) is already palindromic, needing 0 flips.",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "minFlips",
    "params": [("grid", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(grid), len(grid[0])
        row_flips = 0
        for r in range(m):
            row = grid[r]
            for c in range(n // 2):
                if row[c] != row[n - 1 - c]:
                    row_flips += 1
        col_flips = 0
        for c in range(n):
            for r in range(m // 2):
                if grid[r][c] != grid[m - 1 - r][c]:
                    col_flips += 1
        return min(row_flips, col_flips)""",
    "java": """        int m = grid.length, n = grid[0].length;
        int rowFlips = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n / 2; c++) {
                if (grid[r][c] != grid[r][n - 1 - c]) rowFlips++;
            }
        }
        int colFlips = 0;
        for (int c = 0; c < n; c++) {
            for (int r = 0; r < m / 2; r++) {
                if (grid[r][c] != grid[m - 1 - r][c]) colFlips++;
            }
        }
        return Math.min(rowFlips, colFlips);""",
    "visible": [
        {"grid": [[1, 0, 0], [0, 0, 0], [0, 0, 1]]},
        {"grid": [[0, 1], [0, 1], [0, 0]]},
        {"grid": [[1], [0]]},
    ],
    "hidden": [
        {"grid": [[0]]},
        {"grid": [[1, 0, 1, 0]]},
        {"grid": [[1, 1], [0, 0]]},
        {"grid": [[1, 0], [0, 1]]},
        {"grid": [[1, 0, 1], [0, 1, 0], [1, 0, 1]]},
        {"grid": [[0, 1, 0, 1], [1, 0, 1, 0], [0, 1, 0, 1], [1, 0, 1, 0]]},
        {"grid": [[1, 1, 0, 1, 1], [0, 0, 1, 0, 0], [1, 0, 0, 0, 1]]},
        {"grid": _rng_bin_grid(3501, 20, 25, 0.5)},
        {"grid": _rng_bin_grid(3502, 45, 45, 0.5)},
    ],
})

# ============================================================================
# Subtopic 3: 2D Search (36 - 41)
# ============================================================================

TASKS.append({
    "slug": "36-k-weakest-rows-in-a-matrix",
    "title": "The K Weakest Rows in a Matrix",
    "difficulty": "Easy",
    "subtopic": "2D Search",
    "companies": ["Amazon", "Google", "Apple", "Bloomberg"],
    "desc": (
        "You are given an `m x n` binary matrix `mat` of `1`s (representing soldiers) and `0`s (representing civilians). "
        "In every row, all `1`s appear strictly to the left of all `0`s.\n\n"
        "A row `i` is **weaker** than a row `j` if either:\n"
        "- The number of soldiers in row `i` is strictly less than the number of soldiers in row `j`, or\n"
        "- Both rows have the same number of soldiers and `i < j`.\n\n"
        "Return the indices of the `k` weakest rows in the matrix ordered from weakest to strongest."
    ),
    "cons": [
        "m == mat.length",
        "n == mat[i].length",
        "2 <= n, m <= 100",
        "1 <= k <= m",
        "Each row consists of some number of 1s followed by some number of 0s.",
    ],
    "hints": [
        "Because every row has all 1s before all 0s, binary search finds the soldier count of each row in O(log n) time.",
        "Sort the (soldierCount, rowIndex) pairs and take the first k row indices.",
    ],
    "explanations": [
        "Soldier counts per row are [2, 4, 1, 2, 5]; the 3 weakest rows are 2 (1), 0 (2), and 3 (2).",
        "Soldier counts are [1, 4, 1, 1]; the 2 weakest rows by index tie-breaking are 0 and 2.",
        "All rows have 0 soldiers, so the weakest 2 rows are simply 0 and 1.",
    ],
    "time": "O(m * (log n + log m))",
    "space": "O(m)",
    "method": "kWeakestRows",
    "params": [("mat", "int[][]"), ("k", "int")],
    "ret": "int[]",
    "py": """        m, n = len(mat), len(mat[0])
        strengths = []
        for r in range(m):
            row = mat[r]
            lo, hi = 0, n
            while lo < hi:
                mid = (lo + hi) // 2
                if row[mid] == 1:
                    lo = mid + 1
                else:
                    hi = mid
            strengths.append((lo, r))
        strengths.sort()
        return [r for _, r in strengths[:k]]""",
    "java": """        int m = mat.length, n = mat[0].length;
        int[][] pairs = new int[m][2];
        for (int r = 0; r < m; r++) {
            int lo = 0, hi = n;
            while (lo < hi) {
                int mid = (lo + hi) >>> 1;
                if (mat[r][mid] == 1) lo = mid + 1;
                else hi = mid;
            }
            pairs[r][0] = lo;
            pairs[r][1] = r;
        }
        Arrays.sort(pairs, (a, b) -> a[0] != b[0] ? Integer.compare(a[0], b[0]) : Integer.compare(a[1], b[1]));
        int[] res = new int[k];
        for (int i = 0; i < k; i++) res[i] = pairs[i][1];
        return res;""",
    "visible": [
        {"mat": [[1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]], "k": 3},
        {"mat": [[1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0]], "k": 2},
        {"mat": [[0, 0], [0, 0], [0, 0]], "k": 2},
    ],
    "hidden": [
        {"mat": [[1, 1], [1, 1]], "k": 1},
        {"mat": [[1, 1], [1, 1]], "k": 2},
        {"mat": [[1, 1, 1], [1, 1, 0], [1, 0, 0], [0, 0, 0]], "k": 4},
        {"mat": [[0, 0, 0], [1, 0, 0], [1, 1, 0], [1, 1, 1]], "k": 3},
        {"mat": [[1, 0], [0, 0], [1, 1], [0, 0], [1, 0]], "k": 5},
        {"mat": [[1, 1, 1, 0, 0], [1, 1, 1, 0, 0], [1, 1, 1, 0, 0]], "k": 2},
        {"mat": _rng_sorted_rows_bin(3601, 10, 12, ones_first=True), "k": 5},
        {"mat": _rng_sorted_rows_bin(3602, 25, 30, ones_first=True), "k": 12},
        {"mat": _rng_sorted_rows_bin(3603, 50, 50, ones_first=True), "k": 20},
    ],
})

TASKS.append({
    "slug": "37-leftmost-column-with-at-least-a-one",
    "title": "Leftmost Column With a One",
    "difficulty": "Medium",
    "subtopic": "2D Search",
    "companies": ["Meta", "Google", "Amazon", "Microsoft"],
    "desc": (
        "You are given an `m x n` row-sorted binary matrix `mat` where every element is `0` or `1`, and every row "
        "is sorted in non-decreasing order (all `0`s appear before all `1`s in each row).\n\n"
        "Return the 0-indexed column number of the **leftmost** column that contains at least one `1`. If the "
        "matrix contains no `1`s at all, return `-1`."
    ),
    "cons": [
        "m == mat.length",
        "n == mat[i].length",
        "1 <= m, n <= 100",
        "mat[i][j] is either 0 or 1, and every row is sorted in non-decreasing order.",
    ],
    "hints": [
        "Start at the top-right corner (r = 0, c = n - 1).",
        "Whenever mat[r][c] == 1, record c as a better answer and step left (c -= 1); whenever mat[r][c] == 0, step down (r += 1) since no earlier column in row r can hold a 1.",
    ],
    "explanations": [
        "Column 0 has a 1 at row 1, so the leftmost column with a 1 is 0.",
        "Column 1 is the earliest column containing a 1 (at row 0).",
        "The entire matrix consists of zeros, so return -1.",
    ],
    "time": "O(m + n)",
    "space": "O(1)",
    "method": "leftmostColumnWithOne",
    "params": [("mat", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(mat), len(mat[0])
        r, c = 0, n - 1
        ans = -1
        while r < m and c >= 0:
            if mat[r][c] == 1:
                ans = c
                c -= 1
            else:
                r += 1
        return ans""",
    "java": """        int m = mat.length, n = mat[0].length;
        int r = 0, c = n - 1, ans = -1;
        while (r < m && c >= 0) {
            if (mat[r][c] == 1) {
                ans = c;
                c--;
            } else {
                r++;
            }
        }
        return ans;""",
    "visible": [
        {"mat": [[0, 0], [1, 1]]},
        {"mat": [[0, 1], [0, 0]]},
        {"mat": [[0, 0], [0, 0]]},
    ],
    "hidden": [
        {"mat": [[1]]},
        {"mat": [[0]]},
        {"mat": [[0, 0, 0, 1], [0, 0, 1, 1], [0, 1, 1, 1]]},
        {"mat": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]},
        {"mat": [[1, 1, 1], [0, 0, 0], [0, 0, 0]]},
        {"mat": [[0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 1, 1, 1, 1], [0, 0, 0, 0, 0]]},
        {"mat": [[0] * 10 for _ in range(10)]},
        {"mat": _rng_sorted_rows_bin(3701, 20, 25, ones_first=False)},
        {"mat": _rng_sorted_rows_bin(3702, 50, 50, ones_first=False)},
    ],
})

TASKS.append({
    "slug": "38-smallest-rectangle-enclosing-black-pixels",
    "title": "Smallest Rectangle Enclosing Black Pixels",
    "difficulty": "Hard",
    "subtopic": "2D Search",
    "companies": ["Google", "Meta", "Apple", "Bloomberg"],
    "desc": (
        "You are given an `m x n` binary character matrix `image` where `'0'` represents a white pixel and `'1'` "
        "represents a black pixel. All black pixels in `image` form a single 4-directionally connected component.\n\n"
        "Given two integers `x` and `y` representing the coordinates of one known black pixel (`image[x][y] == '1'`), "
        "return the area of the smallest axis-aligned rectangle that encloses all black pixels in `image`."
    ),
    "cons": [
        "m == image.length",
        "n == image[i].length",
        "1 <= m, n <= 100",
        "image[i][j] is either '0' or '1'.",
        "0 <= x < m, 0 <= y < n, and image[x][y] == '1'.",
        "All '1' pixels form a single 4-directionally connected region.",
    ],
    "hints": [
        "Because all black pixels are connected, the rows containing at least one '1' form a contiguous range [top, bottom] containing x, and the columns containing at least one '1' form a contiguous range [left, right] containing y.",
        "Run four binary searches—on [0, x] for top, [x, m - 1] for bottom, [0, y] for left, and [y, n - 1] for right—to find the exact bounding box in O(m log n + n log m) time.",
    ],
    "explanations": [
        "The black pixels occupy rows 0..2 and columns 1..2, forming a 3x2 rectangle of area 6.",
        "The single black pixel at (0, 0) has bounding box area 1.",
        "The connected '1's span rows 1..3 and columns 0..3, giving a 3x4 rectangle of area 12.",
    ],
    "time": "O(m * log n + n * log m)",
    "space": "O(1)",
    "method": "minArea",
    "params": [("image", "char[][]"), ("x", "int"), ("y", "int")],
    "ret": "int",
    "py": """        m, n = len(image), len(image[0])

        def row_has_one(r: int) -> bool:
            return '1' in image[r]

        def col_has_one(c: int) -> bool:
            for r in range(m):
                if image[r][c] == '1':
                    return True
            return False

        # Find top in [0, x]
        lo, hi = 0, x
        while lo < hi:
            mid = (lo + hi) // 2
            if row_has_one(mid):
                hi = mid
            else:
                lo = mid + 1
        top = lo

        # Find bottom in [x, m - 1]
        lo, hi = x, m - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if row_has_one(mid):
                lo = mid
            else:
                hi = mid - 1
        bottom = lo

        # Find left in [0, y]
        lo, hi = 0, y
        while lo < hi:
            mid = (lo + hi) // 2
            if col_has_one(mid):
                hi = mid
            else:
                lo = mid + 1
        left = lo

        # Find right in [y, n - 1]
        lo, hi = y, n - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if col_has_one(mid):
                lo = mid
            else:
                hi = mid - 1
        right = lo

        return (bottom - top + 1) * (right - left + 1)""",
    "java": """        int m = image.length, n = image[0].length;
        int lo = 0, hi = x;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (rowHasOne(image, mid)) hi = mid;
            else lo = mid + 1;
        }
        int top = lo;

        lo = x; hi = m - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >>> 1;
            if (rowHasOne(image, mid)) lo = mid;
            else hi = mid - 1;
        }
        int bottom = lo;

        lo = 0; hi = y;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (colHasOne(image, mid)) hi = mid;
            else lo = mid + 1;
        }
        int left = lo;

        lo = y; hi = n - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >>> 1;
            if (colHasOne(image, mid)) lo = mid;
            else hi = mid - 1;
        }
        int right = lo;

        return (bottom - top + 1) * (right - left + 1);""",
    "java_helpers": """    private boolean rowHasOne(char[][] image, int r) {
        for (char ch : image[r]) if (ch == '1') return true;
        return false;
    }

    private boolean colHasOne(char[][] image, int c) {
        for (int r = 0; r < image.length; r++) if (image[r][c] == '1') return true;
        return false;
    }""",
    "visible": [
        {"image": _grid_from_rows(["0010", "0110", "0100"]), "x": 0, "y": 2},
        {"image": _grid_from_rows(["1"]), "x": 0, "y": 0},
        {"image": _grid_from_rows(["00000", "01100", "11000", "01110"]), "x": 1, "y": 1},
    ],
    "hidden": [
        {"image": _grid_from_rows(["000", "010", "000"]), "x": 1, "y": 1},
        {"image": _grid_from_rows(["11111"]), "x": 0, "y": 4},
        {"image": _grid_from_rows(["1", "1", "1", "1"]), "x": 2, "y": 0},
        {"image": _grid_from_rows(["111", "111", "111"]), "x": 0, "y": 0},
        {"image": _grid_from_rows(["00001", "00011", "00110", "01100", "11000"]), "x": 2, "y": 2},
        {"image": _grid_from_rows(["000000", "011110", "010010", "010010", "011110", "000000"]), "x": 1, "y": 4},
        {"image": (g38a := _connected_black_grid(12, 15, 2, 9, 3, 12, 3801))[0], "x": g38a[1], "y": g38a[2]},
        {"image": (g38b := _connected_black_grid(20, 20, 0, 19, 5, 14, 3802))[0], "x": g38b[1], "y": g38b[2]},
        {"image": (g38c := _connected_black_grid(40, 40, 4, 34, 7, 36, 3803))[0], "x": g38c[1], "y": g38c[2]},
    ],
})

TASKS.append({
    "slug": "39-count-submatrices-with-all-ones",
    "title": "Count Submatrices With All Ones",
    "difficulty": "Medium",
    "subtopic": "2D Search",
    "companies": ["Google", "Amazon", "Meta", "Microsoft"],
    "desc": (
        "Given an `m x n` binary matrix `mat` containing only `0`s and `1`s, return the total number of "
        "non-empty rectangular submatrices whose elements are all `1`."
    ),
    "cons": [
        "m == mat.length",
        "n == mat[i].length",
        "1 <= m, n <= 150",
        "mat[i][j] is either 0 or 1.",
    ],
    "hints": [
        "Treat each row r as the bottom edge of a histogram where height[c] is the number of consecutive 1s ending at (r, c) moving upward.",
        "Use a monotonic increasing stack of column indices along each row to compute, in O(n) time, the number of all-ones submatrices whose bottom-right corner is (r, c).",
    ],
    "explanations": [
        "There are 6 1x1, 2 1x2, 3 2x1, 1 2x2, and 1 3x1 all-ones submatrices, totaling 13.",
        "Summing across all valid all-ones rectangles in the 3x4 grid yields 24.",
        "A 1x1 matrix of [0] has 0 all-ones submatrices.",
    ],
    "time": "O(m * n)",
    "space": "O(n)",
    "method": "numSubmat",
    "params": [("mat", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(mat), len(mat[0])
        heights = [0] * n
        total = 0
        for r in range(m):
            for c in range(n):
                heights[c] = heights[c] + 1 if mat[r][c] == 1 else 0
            stack = []
            row_sum = [0] * n
            for c in range(n):
                while stack and heights[stack[-1]] >= heights[c]:
                    stack.pop()
                if stack:
                    prev = stack[-1]
                    row_sum[c] = row_sum[prev] + heights[c] * (c - prev)
                else:
                    row_sum[c] = heights[c] * (c + 1)
                stack.append(c)
                total += row_sum[c]
        return total""",
    "java": """        int m = mat.length, n = mat[0].length;
        int[] heights = new int[n];
        int[] stack = new int[n];
        int[] rowSum = new int[n];
        int total = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                heights[c] = mat[r][c] == 1 ? heights[c] + 1 : 0;
            }
            int top = -1;
            for (int c = 0; c < n; c++) {
                while (top >= 0 && heights[stack[top]] >= heights[c]) top--;
                if (top >= 0) {
                    int prev = stack[top];
                    rowSum[c] = rowSum[prev] + heights[c] * (c - prev);
                } else {
                    rowSum[c] = heights[c] * (c + 1);
                }
                stack[++top] = c;
                total += rowSum[c];
            }
        }
        return total;""",
    "visible": [
        {"mat": [[1, 0, 1], [1, 1, 0], [1, 1, 0]]},
        {"mat": [[0, 1, 1, 0], [0, 1, 1, 1], [1, 1, 1, 0]]},
        {"mat": [[0]]},
    ],
    "hidden": [
        {"mat": [[1]]},
        {"mat": [[1, 1, 1, 1]]},
        {"mat": [[1], [1], [1], [1]]},
        {"mat": [[1, 1], [1, 1]]},
        {"mat": [[1, 0, 1], [0, 1, 0], [1, 0, 1]]},
        {"mat": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]},
        {"mat": [[1] * 6 for _ in range(5)]},
        {"mat": _rng_bin_grid(3901, 15, 15, 0.7)},
        {"mat": _rng_bin_grid(3902, 40, 40, 0.65)},
    ],
})

TASKS.append({
    "slug": "40-max-sum-of-rectangle-no-larger-than-k",
    "title": "Max Sum of Rectangle No Larger Than K",
    "difficulty": "Hard",
    "subtopic": "2D Search",
    "companies": ["Google", "Meta", "Amazon", "Goldman Sachs"],
    "desc": (
        "Given an `m x n` integer `matrix` and an integer `k`, return the maximum sum of any non-empty rectangular "
        "submatrix such that its sum is no larger than `k` (i.e., `sum <= k`).\n\n"
        "It is guaranteed that at least one rectangular submatrix has a sum less than or equal to `k`."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 100",
        "-100 <= matrix[i][j] <= 100",
        "-10^5 <= k <= 10^5",
    ],
    "hints": [
        "Fix a pair of top and bottom rows (or left and right columns, whichever dimension is smaller) and collapse the band into a 1D array of column sums.",
        "For the 1D array, first check Kadane's maximum subarray sum: if it is <= k, you're done for this band; otherwise use a sorted structure of prefix sums to find the smallest previous prefix >= currentPrefix - k.",
    ],
    "explanations": [
        "The submatrix [[0, 1], [-2, 3]] has sum 2, which equals k = 2.",
        "The entire 1x3 submatrix [2, 2, -1] has sum 3, matching k = 3.",
        "Only submatrices containing -5 have sum <= -3; the best is [-5, 2] with sum -3.",
    ],
    "time": "O(min(m, n)^2 * max(m, n) * log(max(m, n)))",
    "space": "O(max(m, n))",
    "method": "maxSumSubmatrix",
    "params": [("matrix", "int[][]"), ("k", "int")],
    "ret": "int",
    "py": """        import bisect
        m, n = len(matrix), len(matrix[0])
        if m > n:
            matrix = [[matrix[r][c] for r in range(m)] for c in range(n)]
            m, n = n, m
        ans = -10**18
        for top in range(m):
            col_sums = [0] * n
            for bottom in range(top, m):
                row = matrix[bottom]
                for c in range(n):
                    col_sums[c] += row[c]
                # Fast-path with Kadane's algorithm
                cur = col_sums[0]
                best_k = cur
                for x in col_sums[1:]:
                    cur = x if cur < 0 else cur + x
                    if cur > best_k:
                        best_k = cur
                if best_k <= k:
                    if best_k > ans:
                        ans = best_k
                    if ans == k:
                        return k
                    continue
                prefixes = [0]
                pref = 0
                for x in col_sums:
                    pref += x
                    idx = bisect.bisect_left(prefixes, pref - k)
                    if idx < len(prefixes):
                        cand = pref - prefixes[idx]
                        if cand > ans:
                            ans = cand
                            if ans == k:
                                return k
                    bisect.insort(prefixes, pref)
        return ans""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        int[][] mat = matrix;
        if (m > n) {
            mat = new int[n][m];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    mat[c][r] = matrix[r][c];
            int tmp = m; m = n; n = tmp;
        }
        int ans = Integer.MIN_VALUE;
        for (int top = 0; top < m; top++) {
            int[] colSums = new int[n];
            for (int bottom = top; bottom < m; bottom++) {
                int[] row = mat[bottom];
                for (int c = 0; c < n; c++) colSums[c] += row[c];
                int cur = colSums[0], bestK = cur;
                for (int c = 1; c < n; c++) {
                    cur = cur < 0 ? colSums[c] : cur + colSums[c];
                    if (cur > bestK) bestK = cur;
                }
                if (bestK <= k) {
                    if (bestK > ans) ans = bestK;
                    if (ans == k) return k;
                    continue;
                }
                TreeSet<Integer> set = new TreeSet<>();
                set.add(0);
                int pref = 0;
                for (int x : colSums) {
                    pref += x;
                    Integer ceil = set.ceiling(pref - k);
                    if (ceil != null) {
                        int cand = pref - ceil;
                        if (cand > ans) {
                            ans = cand;
                            if (ans == k) return k;
                        }
                    }
                    set.add(pref);
                }
            }
        }
        return ans;""",
    "visible": [
        {"matrix": [[1, 0, 1], [0, -2, 3]], "k": 2},
        {"matrix": [[2, 2, -1]], "k": 3},
        {"matrix": [[-5, 2, 4]], "k": -3},
    ],
    "hidden": [
        {"matrix": [[-1]], "k": -1},
        {"matrix": [[2, 2, -1]], "k": 0},
        {"matrix": [[5, -4, -3, 4], [-3, -4, 4, 5], [5, 1, 5, -4]], "k": 8},
        {"matrix": [[5, -4, -3, 4], [-3, -4, 4, 5], [5, 1, 5, -4]], "k": 3},
        {"matrix": [[-2, -3], [-4, -5]], "k": -1},
        {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "k": 14},
        {"matrix": [[10, -2, 5], [-3, 7, -1], [4, -6, 8], [2, 3, -9]], "k": 12},
        {"matrix": _rng_int_grid(4001, 15, 20, -50, 50), "k": 137},
        {"matrix": _rng_int_grid(4002, 28, 35, -100, 100), "k": 250},
    ],
})

TASKS.append({
    "slug": "41-largest-magic-square",
    "title": "Largest Magic Square",
    "difficulty": "Medium",
    "subtopic": "2D Search",
    "companies": ["Google", "Amazon", "Adobe", "Bloomberg"],
    "desc": (
        "A `k x k` **magic square** is a `k x k` subgrid filled with integers such that every row sum, every "
        "column sum, and both main diagonal sums are all equal. The integers in the magic square do not need to "
        "be distinct. Every `1 x 1` cell is trivially a magic square of side length `1`.\n\n"
        "Given an `m x n` integer `grid`, return the side length `k` of the **largest** magic square that appears "
        "as a contiguous subgrid of `grid`."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 50",
        "1 <= grid[i][j] <= 10^6",
    ],
    "hints": [
        "Precompute row prefix sums and column prefix sums so any horizontal or vertical segment sum can be queried in O(1).",
        "Search side lengths k from min(m, n) downward to 2; the very first valid k x k magic square found is immediately the answer.",
    ],
    "explanations": [
        "The 3x3 subgrid in rows 1..3 and columns 1..3 ([[5,1,6],[5,4,3],[2,7,3]]) has every row, column, and diagonal summing to 12.",
        "The 2x2 subgrid [[3,3],[3,3]] is a valid magic square of side length 2.",
        "No 2x2 subgrid has equal row, column, and diagonal sums, so the largest magic square has side length 1.",
    ],
    "time": "O(m * n * min(m, n)^2)",
    "space": "O(m * n)",
    "method": "largestMagicSquare",
    "params": [("grid", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(grid), len(grid[0])
        row_pref = [[0] * (n + 1) for _ in range(m)]
        col_pref = [[0] * n for _ in range(m + 1)]
        for r in range(m):
            for c in range(n):
                row_pref[r][c + 1] = row_pref[r][c] + grid[r][c]
                col_pref[r + 1][c] = col_pref[r][c] + grid[r][c]

        for k in range(min(m, n), 1, -1):
            for r in range(m - k + 1):
                for c in range(n - k + 1):
                    target = row_pref[r][c + k] - row_pref[r][c]
                    ok = True
                    for i in range(1, k):
                        if row_pref[r + i][c + k] - row_pref[r + i][c] != target:
                            ok = False
                            break
                    if not ok:
                        continue
                    for j in range(k):
                        if col_pref[r + k][c + j] - col_pref[r][c + j] != target:
                            ok = False
                            break
                    if not ok:
                        continue
                    d1 = d2 = 0
                    for i in range(k):
                        d1 += grid[r + i][c + i]
                        d2 += grid[r + i][c + k - 1 - i]
                    if d1 == target and d2 == target:
                        return k
        return 1""",
    "java": """        int m = grid.length, n = grid[0].length;
        long[][] rowPref = new long[m][n + 1];
        long[][] colPref = new long[m + 1][n];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                rowPref[r][c + 1] = rowPref[r][c] + grid[r][c];
                colPref[r + 1][c] = colPref[r][c] + grid[r][c];
            }
        }
        for (int k = Math.min(m, n); k >= 2; k--) {
            for (int r = 0; r <= m - k; r++) {
                for (int c = 0; c <= n - k; c++) {
                    long target = rowPref[r][c + k] - rowPref[r][c];
                    boolean ok = true;
                    for (int i = 1; i < k; i++) {
                        if (rowPref[r + i][c + k] - rowPref[r + i][c] != target) {
                            ok = false;
                            break;
                        }
                    }
                    if (!ok) continue;
                    for (int j = 0; j < k; j++) {
                        if (colPref[r + k][c + j] - colPref[r][c + j] != target) {
                            ok = false;
                            break;
                        }
                    }
                    if (!ok) continue;
                    long d1 = 0, d2 = 0;
                    for (int i = 0; i < k; i++) {
                        d1 += grid[r + i][c + i];
                        d2 += grid[r + i][c + k - 1 - i];
                    }
                    if (d1 == target && d2 == target) return k;
                }
            }
        }
        return 1;""",
    "visible": [
        {"grid": [[7, 1, 4, 5, 6], [2, 5, 1, 6, 4], [1, 5, 4, 3, 2], [1, 2, 7, 3, 4]]},
        {"grid": [[5, 1, 3, 1], [9, 3, 3, 1], [1, 3, 3, 8]]},
        {"grid": [[1, 2, 3], [4, 5, 6]]},
    ],
    "hidden": [
        {"grid": [[42]]},
        {"grid": [[8, 1, 6], [3, 5, 7], [4, 9, 2]]},
        {"grid": [[16, 3, 2, 13], [5, 10, 11, 8], [9, 6, 7, 12], [4, 15, 14, 1]]},
        {"grid": [[2, 2, 2], [2, 2, 2], [2, 2, 2]]},
        {"grid": [[1, 2], [2, 1]]},
        {"grid": [[1000000, 1000000], [1000000, 1000000]]},
        {"grid": [[9, 9, 9, 9, 9], [9, 8, 1, 6, 9], [9, 3, 5, 7, 9], [9, 4, 9, 2, 9], [9, 9, 9, 9, 9]]},
        {"grid": _rng_int_grid(4101, 15, 15, 1, 3)},
        {"grid": [[7] * 25 for _ in range(25)]},
    ],
})

# ============================================================================
# Subtopic 4: Simulation (42 - 47)
# ============================================================================

TASKS.append({
    "slug": "42-where-will-the-ball-fall",
    "title": "Where Will the Ball Fall",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Google", "Amazon", "Meta", "Uber"],
    "desc": (
        "You have a 2D box of size `m x n` represented by an integer matrix `grid`, open at both the top and bottom. "
        "Each cell contains a diagonal board spanning two opposite corners:\n"
        "- `1` redirects a ball to the **right** (from top-left to bottom-right).\n"
        "- `-1` redirects a ball to the **left** (from top-right to bottom-left).\n\n"
        "We drop `n` balls simultaneously, one at the top of each column `0, 1, ..., n - 1`. A ball gets stuck and "
        "cannot fall further if it hits either side wall of the box or lands in a `'V'`-shaped pocket formed by a "
        "`1` immediately to the left of a `-1`.\n\n"
        "Return an integer array `answer` of length `n`, where `answer[j]` is the column where the ball dropped from "
        "column `j` exits the bottom, or `-1` if it gets stuck."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 100",
        "grid[i][j] is either 1 or -1.",
    ],
    "hints": [
        "Simulate each ball independently from row 0 down to row m - 1, tracking its current column col.",
        "At cell (r, col) with direction d = grid[r][col], the ball advances to nextCol = col + d only if 0 <= nextCol < n and grid[r][nextCol] == d; otherwise it gets stuck.",
    ],
    "explanations": [
        "Only the ball dropped at column 0 navigates through all 5 rows and exits at column 1; all other balls get trapped in V-pockets or walls.",
        "A single column box always pushes the ball into a side wall, returning [-1].",
        "The first five balls exit cleanly at columns 0 through 4, while the ball dropped at column 5 hits the right wall on row 0 and returns -1.",
    ],
    "time": "O(m * n)",
    "space": "O(n)",
    "method": "findBall",
    "params": [("grid", "int[][]")],
    "ret": "int[]",
    "py": """        m, n = len(grid), len(grid[0])
        ans = [-1] * n
        for start in range(n):
            col = start
            for r in range(m):
                d = grid[r][col]
                nxt = col + d
                if nxt < 0 or nxt >= n or grid[r][nxt] != d:
                    col = -1
                    break
                col = nxt
            ans[start] = col
        return ans""",
    "java": """        int m = grid.length, n = grid[0].length;
        int[] ans = new int[n];
        for (int start = 0; start < n; start++) {
            int col = start;
            for (int r = 0; r < m; r++) {
                int d = grid[r][col];
                int nxt = col + d;
                if (nxt < 0 || nxt >= n || grid[r][nxt] != d) {
                    col = -1;
                    break;
                }
                col = nxt;
            }
            ans[start] = col;
        }
        return ans;""",
    "visible": [
        {"grid": [[1, 1, 1, -1, -1], [1, 1, 1, -1, -1], [-1, -1, -1, 1, 1], [1, 1, 1, 1, -1], [-1, -1, -1, -1, -1]]},
        {"grid": [[-1]]},
        {"grid": [[1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1], [1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1]]},
    ],
    "hidden": [
        {"grid": [[1]]},
        {"grid": [[1, 1], [-1, -1]]},
        {"grid": [[1, -1], [-1, 1]]},
        {"grid": [[-1, 1], [1, -1]]},
        {"grid": [[1, 1, 1, 1]]},
        {"grid": [[-1, -1, -1, -1]]},
        {"grid": [[1, 1, -1, -1], [1, 1, -1, -1], [1, 1, -1, -1]]},
        {"grid": _rng_ball_grid(4201, 15, 20)},
        {"grid": _rng_ball_grid(4202, 40, 40)},
    ],
})

TASKS.append({
    "slug": "43-image-smoother-filter",
    "title": "Image Smoother Filter",
    "difficulty": "Easy",
    "subtopic": "Simulation",
    "companies": ["Amazon", "Apple", "Microsoft", "Adobe"],
    "desc": (
        "An image smoother is a `3 x 3` averaging filter applied to every pixel of an `m x n` grayscale integer "
        "matrix `img`.\n\n"
        "The smoothed value at cell `(r, c)` is the **floor** of the average of `(r, c)` and all of its valid "
        "in-bounds 8-directional neighbors (corners average 4 cells, non-corner borders average 6 cells, and interior "
        "cells average 9 cells; single-row or single-column grids average fewer cells accordingly).\n\n"
        "Return the smoothed `m x n` integer matrix."
    ),
    "cons": [
        "m == img.length",
        "n == img[i].length",
        "1 <= m, n <= 100",
        "0 <= img[i][j] <= 255",
    ],
    "hints": [
        "For each cell (r, c), loop over nr in [max(0, r - 1), min(m - 1, r + 1)] and nc in [max(0, c - 1), min(n - 1, c + 1)].",
        "Accumulate both the sum and the count of valid cells, then store sum // count in a new result matrix so updates do not affect neighbor reads.",
    ],
    "explanations": [
        "Every corner averages 3 ones and 1 zero (floor(3/4) = 0), every edge averages 5 ones and 1 zero (floor(5/6) = 0), and the center averages 8 ones and 1 zero (floor(8/9) = 0).",
        "Averaging each 3x3 neighborhood of [[100,200,100],[200,50,200],[100,200,100]] produces [[137,141,137],[141,138,141],[137,141,137]].",
        "A 1x1 image has only itself in its neighborhood, so its value stays unchanged.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "imageSmoother",
    "params": [("img", "int[][]")],
    "ret": "int[][]",
    "py": """        m, n = len(img), len(img[0])
        res = [[0] * n for _ in range(m)]
        for r in range(m):
            r0, r1 = max(0, r - 1), min(m - 1, r + 1)
            for c in range(n):
                c0, c1 = max(0, c - 1), min(n - 1, c + 1)
                total = 0
                cnt = 0
                for nr in range(r0, r1 + 1):
                    row = img[nr]
                    for nc in range(c0, c1 + 1):
                        total += row[nc]
                        cnt += 1
                res[r][c] = total // cnt
        return res""",
    "java": """        int m = img.length, n = img[0].length;
        int[][] res = new int[m][n];
        for (int r = 0; r < m; r++) {
            int r0 = Math.max(0, r - 1), r1 = Math.min(m - 1, r + 1);
            for (int c = 0; c < n; c++) {
                int c0 = Math.max(0, c - 1), c1 = Math.min(n - 1, c + 1);
                int total = 0, cnt = 0;
                for (int nr = r0; nr <= r1; nr++) {
                    for (int nc = c0; nc <= c1; nc++) {
                        total += img[nr][nc];
                        cnt++;
                    }
                }
                res[r][c] = total / cnt;
            }
        }
        return res;""",
    "visible": [
        {"img": [[1, 1, 1], [1, 0, 1], [1, 1, 1]]},
        {"img": [[100, 200, 100], [200, 50, 200], [100, 200, 100]]},
        {"img": [[255]]},
    ],
    "hidden": [
        {"img": [[0]]},
        {"img": [[10, 20, 30, 40]]},
        {"img": [[10], [20], [30], [40]]},
        {"img": [[255, 255], [255, 255]]},
        {"img": [[0, 255], [255, 0]]},
        {"img": [[2, 3, 4], [5, 6, 7], [8, 9, 10], [11, 12, 13]]},
        {"img": [[255, 0, 255, 0], [0, 255, 0, 255], [255, 0, 255, 0]]},
        {"img": _rng_int_grid(4301, 12, 15, 0, 255)},
        {"img": _rng_int_grid(4302, 35, 35, 0, 255)},
    ],
})

TASKS.append({
    "slug": "44-grid-match-three-cascade",
    "title": "Grid Match-Three Cascade",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Bloomberg", "Google", "Meta", "Apple"],
    "desc": (
        "You are given an `m x n` integer matrix `board` representing a puzzle grid of colored tiles. A positive "
        "integer `board[r][c] > 0` represents a tile type, and `0` represents an empty cell.\n\n"
        "Repeatedly perform the following stabilization round until no more tiles can be crushed:\n"
        "1. **Crush**: If three or more tiles of the same positive type are adjacent horizontally or vertically, "
        "mark all such tiles simultaneously and replace them with `0`.\n"
        "2. **Gravity**: After crushing, all remaining positive tiles fall downward in their respective columns to "
        "fill any empty cells below them, leaving `0`s at the top of each column.\n\n"
        "Return the final stable `board`."
    ),
    "cons": [
        "m == board.length",
        "n == board[i].length",
        "3 <= m, n <= 50",
        "0 <= board[i][j] <= 2000",
    ],
    "hints": [
        "Mark all horizontal and vertical runs of length >= 3 in a separate boolean matrix before clearing any cells, so overlapping L- or T-shaped matches are both detected.",
        "For gravity, sweep each column from bottom to top with a write pointer copying non-zero values downward and filling remaining top slots with 0.",
    ],
    "explanations": [
        "Three 1s in the bottom row crush and the tiles above drop down, triggering no further matches.",
        "The vertical column of three 2s and horizontal row of three 2s crush simultaneously, letting the top tiles drop.",
        "No three identical positive tiles are adjacent horizontally or vertically, so the board is already stable.",
    ],
    "time": "O((m * n)^2)",
    "space": "O(m * n)",
    "method": "candyCrush",
    "params": [("board", "int[][]")],
    "ret": "int[][]",
    "py": """        m, n = len(board), len(board[0])
        g = [row[:] for row in board]
        while True:
            crush = [[False] * n for _ in range(m)]
            changed = False
            for r in range(m):
                for c in range(n - 2):
                    v = g[r][c]
                    if v != 0 and v == g[r][c + 1] == g[r][c + 2]:
                        crush[r][c] = crush[r][c + 1] = crush[r][c + 2] = True
                        changed = True
            for c in range(n):
                for r in range(m - 2):
                    v = g[r][c]
                    if v != 0 and v == g[r + 1][c] == g[r + 2][c]:
                        crush[r][c] = crush[r + 1][c] = crush[r + 2][c] = True
                        changed = True
            if not changed:
                return g
            for c in range(n):
                write = m - 1
                for r in range(m - 1, -1, -1):
                    if not crush[r][c] and g[r][c] != 0:
                        g[write][c] = g[r][c]
                        write -= 1
                while write >= 0:
                    g[write][c] = 0
                    write -= 1""",
    "java": """        int m = board.length, n = board[0].length;
        int[][] g = new int[m][n];
        for (int r = 0; r < m; r++) g[r] = board[r].clone();
        while (true) {
            boolean[][] crush = new boolean[m][n];
            boolean changed = false;
            for (int r = 0; r < m; r++) {
                for (int c = 0; c < n - 2; c++) {
                    int v = g[r][c];
                    if (v != 0 && v == g[r][c + 1] && v == g[r][c + 2]) {
                        crush[r][c] = crush[r][c + 1] = crush[r][c + 2] = true;
                        changed = true;
                    }
                }
            }
            for (int c = 0; c < n; c++) {
                for (int r = 0; r < m - 2; r++) {
                    int v = g[r][c];
                    if (v != 0 && v == g[r + 1][c] && v == g[r + 2][c]) {
                        crush[r][c] = crush[r + 1][c] = crush[r + 2][c] = true;
                        changed = true;
                    }
                }
            }
            if (!changed) return g;
            for (int c = 0; c < n; c++) {
                int write = m - 1;
                for (int r = m - 1; r >= 0; r--) {
                    if (!crush[r][c] && g[r][c] != 0) {
                        g[write--][c] = g[r][c];
                    }
                }
                while (write >= 0) g[write--][c] = 0;
            }
        }""",
    "visible": [
        {"board": [[3, 4, 5], [2, 3, 4], [1, 1, 1]]},
        {"board": [[5, 2, 6], [7, 2, 8], [2, 2, 2]]},
        {"board": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
    ],
    "hidden": [
        {"board": [[0, 0, 0], [0, 0, 0], [0, 0, 0]]},
        {"board": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]},
        {"board": [[1, 3, 5, 5, 2], [3, 4, 3, 3, 1], [3, 2, 4, 5, 2], [2, 4, 4, 5, 5], [1, 4, 4, 1, 1]]},
        {"board": [[110, 5, 112, 113, 114], [210, 211, 5, 213, 214], [310, 311, 3, 313, 314], [410, 411, 412, 5, 414], [5, 1, 512, 3, 3], [610, 4, 1, 613, 614], [710, 1, 2, 713, 714], [810, 1, 2, 1, 1], [1, 1, 2, 2, 2], [4, 1, 4, 4, 1014]]},
        # Chain reaction: crushing bottom 2s drops three 1s together horizontally
        {"board": [[4, 1, 5], [1, 2, 1], [2, 2, 2], [6, 7, 8]]},
        # Chain reaction vertically
        {"board": [[1, 4, 5], [1, 6, 7], [2, 2, 2], [1, 8, 9]]},
        {"board": [[5, 5, 5, 5], [1, 2, 3, 4], [5, 5, 5, 5]]},
        {"board": _rng_int_grid(4401, 10, 10, 1, 4)},
        {"board": _rng_int_grid(4402, 25, 25, 1, 4)},
    ],
})

TASKS.append({
    "slug": "45-minesweeper-click-reveal",
    "title": "Minesweeper Click Reveal",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Uber", "Amazon", "Meta", "Microsoft"],
    "desc": (
        "You are given an `m x n` character matrix `board` representing a Minesweeper game board:\n"
        "- `'M'`: an unrevealed mine\n"
        "- `'E'`: an unrevealed empty square\n"
        "- `'B'`: a revealed blank square with no adjacent mines\n"
        "- `'1'` to `'8'`: a revealed square showing the count of adjacent mines\n"
        "- `'X'`: a revealed mine\n\n"
        "You are also given an integer array `click = [r, c]` pointing to an unrevealed square (`'M'` or `'E'`). "
        "Update and return the board after clicking `(r, c)`:\n"
        "1. If `(r, c)` is `'M'`, change it to `'X'` and stop.\n"
        "2. If `(r, c)` is `'E'` with at least one adjacent `'M'` (among its 8 neighbors), replace it with the digit `'1'`–`'8'`.\n"
        "3. If `(r, c)` is `'E'` with zero adjacent mines, replace it with `'B'` and recursively reveal all of its unrevealed `'E'` 8-neighbors."
    ),
    "cons": [
        "m == board.length",
        "n == board[i].length",
        "1 <= m, n <= 50",
        "board[i][j] is one of 'M', 'E', 'B', '1'-'8', or 'X'.",
        "click.length == 2, 0 <= click[0] < m, 0 <= click[1] < n",
        "board[click[0]][click[1]] is either 'M' or 'E'.",
    ],
    "hints": [
        "Handle clicking a mine ('M') immediately by setting that cell to 'X' and returning.",
        "Otherwise use BFS or DFS starting from click: count adjacent 'M' cells first; only enqueue/recurse into unrevealed 'E' neighbors when the count is 0, marking them visited right away to avoid duplicates.",
    ],
    "explanations": [
        "Clicking (3, 0) reveals an empty square with 0 adjacent mines, flooding outward until every frontier cell adjacent to the mine at (1, 2) displays '1'.",
        "Clicking directly on the mine at (1, 2) turns it into 'X' and leaves all other cells unchanged.",
        "Clicking (0, 0) next to a mine at (0, 1) only reveals '1' at (0, 0) without expanding further.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "updateBoard",
    "params": [("board", "char[][]"), ("click", "int[]")],
    "ret": "char[][]",
    "py": """        from collections import deque
        m, n = len(board), len(board[0])
        res = [row[:] for row in board]
        sr, sc = click[0], click[1]
        if res[sr][sc] == 'M':
            res[sr][sc] = 'X'
            return res
        q = deque([(sr, sc)])
        visited = [[False] * n for _ in range(m)]
        visited[sr][sc] = True
        while q:
            r, c = q.popleft()
            mines = 0
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and res[nr][nc] == 'M':
                        mines += 1
            if mines > 0:
                res[r][c] = str(mines)
            else:
                res[r][c] = 'B'
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n and not visited[nr][nc] and res[nr][nc] == 'E':
                            visited[nr][nc] = True
                            q.append((nr, nc))
        return res""",
    "java": """        int m = board.length, n = board[0].length;
        char[][] res = new char[m][n];
        for (int r = 0; r < m; r++) res[r] = board[r].clone();
        int sr = click[0], sc = click[1];
        if (res[sr][sc] == 'M') {
            res[sr][sc] = 'X';
            return res;
        }
        boolean[][] visited = new boolean[m][n];
        ArrayDeque<int[]> q = new ArrayDeque<>();
        q.add(new int[]{sr, sc});
        visited[sr][sc] = true;
        while (!q.isEmpty()) {
            int[] cur = q.poll();
            int r = cur[0], c = cur[1];
            int mines = 0;
            for (int dr = -1; dr <= 1; dr++) {
                for (int dc = -1; dc <= 1; dc++) {
                    if (dr == 0 && dc == 0) continue;
                    int nr = r + dr, nc = c + dc;
                    if (nr >= 0 && nr < m && nc >= 0 && nc < n && res[nr][nc] == 'M') {
                        mines++;
                    }
                }
            }
            if (mines > 0) {
                res[r][c] = (char) ('0' + mines);
            } else {
                res[r][c] = 'B';
                for (int dr = -1; dr <= 1; dr++) {
                    for (int dc = -1; dc <= 1; dc++) {
                        if (dr == 0 && dc == 0) continue;
                        int nr = r + dr, nc = c + dc;
                        if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc] && res[nr][nc] == 'E') {
                            visited[nr][nc] = true;
                            q.add(new int[]{nr, nc});
                        }
                    }
                }
            }
        }
        return res;""",
    "visible": [
        {"board": _grid_from_rows(["EEEEE", "EEMEE", "EEEEE", "EEEEE"]), "click": [3, 0]},
        {"board": _grid_from_rows(["B1E1B", "B1M1B", "B111B", "BBBBB"]), "click": [1, 2]},
        {"board": _grid_from_rows(["EM", "EE"]), "click": [0, 0]},
    ],
    "hidden": [
        {"board": _grid_from_rows(["E"]), "click": [0, 0]},
        {"board": _grid_from_rows(["M"]), "click": [0, 0]},
        {"board": _grid_from_rows(["MMM", "MEM", "MMM"]), "click": [1, 1]},
        {"board": _grid_from_rows(["EEEEE"]), "click": [0, 2]},
        {"board": _grid_from_rows(["E", "E", "M", "E", "E"]), "click": [0, 0]},
        {"board": _grid_from_rows(["EEEEE", "EMMME", "EMEME", "EMMME", "EEEEE"]), "click": [0, 0]},
        {"board": _grid_from_rows(["EEEEE", "EMMME", "EMEME", "EMMME", "EEEEE"]), "click": [2, 2]},
        {"board": (g45a := _rng_minesweeper(4501, 12, 12, 18))[0], "click": g45a[1]},
        {"board": (g45b := _rng_minesweeper(4502, 30, 30, 80))[0], "click": g45b[1]},
    ],
})

TASKS.append({
    "slug": "46-suffix-instructions-staying-in-grid",
    "title": "Suffix Instructions Staying in a Grid",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Amazon", "Google", "Salesforce"],
    "desc": (
        "There is an `n x n` grid with top-left cell `(0, 0)` and bottom-right cell `(n - 1, n - 1)`. "
        "You are given `n`, a starting position `startPos = [startRow, startCol]`, and a string `s` of length `m` "
        "consisting of movement commands `'L'` (left), `'R'` (right), `'U'` (up), and `'D'` (down).\n\n"
        "For each starting index `i` from `0` to `m - 1`, suppose the robot begins at `startPos` and executes "
        "instructions `s[i], s[i + 1], ...` one by one, stopping immediately before any instruction that would move "
        "the robot outside the `n x n` grid (or when `s` ends).\n\n"
        "Return an integer array `answer` of length `m`, where `answer[i]` is the number of instructions the robot "
        "can execute starting from index `i`."
    ),
    "cons": [
        "1 <= n <= 500",
        "startPos.length == 2",
        "0 <= startPos[0], startPos[1] < n",
        "1 <= s.length <= 500",
        "s consists only of 'L', 'R', 'U', and 'D'.",
    ],
    "hints": [
        "For each suffix starting at index i, you can simulate step-by-step in O(m) time, giving O(m^2) overall—or optimize to O(m) using backward prefix-displacement hash maps!",
        "With prefix displacements (dr, dc) from the start of s, the robot leaves the grid at the earliest index j >= i where dr[j+1] - dr[i] hits (-startRow - 1) or (n - startRow), or dc[j+1] - dc[i] hits (-startCol - 1) or (n - startCol).",
    ],
    "explanations": [
        "Starting at (0, 1) in a 3x3 grid, the suffixes starting at indices 0..5 stay in bounds for 1, 5, 4, 3, 1, and 0 steps respectively.",
        "Starting at (1, 1) in a 2x2 grid, the suffixes execute 4, 1, 0, and 0 steps.",
        "In a 1x1 grid, any move immediately exits the grid, so every suffix executes 0 instructions.",
    ],
    "time": "O(m)",
    "space": "O(m)",
    "method": "executeInstructions",
    "params": [("n", "int"), ("startPos", "int[]"), ("s", "String")],
    "ret": "int[]",
    "py": """        m = len(s)
        sr, sc = startPos[0], startPos[1]
        # Compute prefix displacements from index 0
        pr = [0] * (m + 1)
        pc = [0] * (m + 1)
        for i, ch in enumerate(s):
            dr = -1 if ch == 'U' else (1 if ch == 'D' else 0)
            dc = -1 if ch == 'L' else (1 if ch == 'R' else 0)
            pr[i + 1] = pr[i] + dr
            pc[i + 1] = pc[i] + dc

        ans = [0] * m
        row_seen = {}
        col_seen = {}
        for i in range(m - 1, -1, -1):
            row_seen[pr[i + 1]] = i + 1
            col_seen[pc[i + 1]] = i + 1
            stop = m + 1
            for target_r in (pr[i] - sr - 1, pr[i] + n - sr):
                if target_r in row_seen and row_seen[target_r] < stop:
                    stop = row_seen[target_r]
            for target_c in (pc[i] - sc - 1, pc[i] + n - sc):
                if target_c in col_seen and col_seen[target_c] < stop:
                    stop = col_seen[target_c]
            ans[i] = stop - 1 - i
        return ans""",
    "java": """        int m = s.length();
        int sr = startPos[0], sc = startPos[1];
        int[] pr = new int[m + 1];
        int[] pc = new int[m + 1];
        for (int i = 0; i < m; i++) {
            char ch = s.charAt(i);
            int dr = ch == 'U' ? -1 : (ch == 'D' ? 1 : 0);
            int dc = ch == 'L' ? -1 : (ch == 'R' ? 1 : 0);
            pr[i + 1] = pr[i] + dr;
            pc[i + 1] = pc[i] + dc;
        }
        int[] ans = new int[m];
        Map<Integer, Integer> rowSeen = new HashMap<>();
        Map<Integer, Integer> colSeen = new HashMap<>();
        for (int i = m - 1; i >= 0; i--) {
            rowSeen.put(pr[i + 1], i + 1);
            colSeen.put(pc[i + 1], i + 1);
            int stop = m + 1;
            Integer t1 = rowSeen.get(pr[i] - sr - 1);
            if (t1 != null && t1 < stop) stop = t1;
            Integer t2 = rowSeen.get(pr[i] + n - sr);
            if (t2 != null && t2 < stop) stop = t2;
            Integer t3 = colSeen.get(pc[i] - sc - 1);
            if (t3 != null && t3 < stop) stop = t3;
            Integer t4 = colSeen.get(pc[i] + n - sc);
            if (t4 != null && t4 < stop) stop = t4;
            ans[i] = stop - 1 - i;
        }
        return ans;""",
    "visible": [
        {"n": 3, "startPos": [0, 1], "s": "RRDDLU"},
        {"n": 2, "startPos": [1, 1], "s": "LURD"},
        {"n": 1, "startPos": [0, 0], "s": "LRUD"},
    ],
    "hidden": [
        {"n": 1, "startPos": [0, 0], "s": "R"},
        {"n": 5, "startPos": [2, 2], "s": "UDLRUDLR"},
        {"n": 3, "startPos": [0, 0], "s": "DDRRUULL"},
        {"n": 4, "startPos": [3, 3], "s": "UUUULLLL"},
        {"n": 2, "startPos": [0, 0], "s": "RDLURDLU"},
        {"n": 10, "startPos": [0, 9], "s": "DDDDDDDDDDLLLLLLLLLL"},
        {"n": 500, "startPos": [250, 250], "s": "LRUD" * 50},
        {"n": 20, "startPos": [10, 10], "s": "".join(random.Random(4601).choice("LRUD") for _ in range(150))},
        {"n": 50, "startPos": [25, 25], "s": "".join(random.Random(4602).choice("LRUD") for _ in range(500))},
    ],
})

TASKS.append({
    "slug": "47-count-battleships-on-a-board",
    "title": "Count Battleships on a Board",
    "difficulty": "Medium",
    "subtopic": "Simulation",
    "companies": ["Meta", "Amazon", "Microsoft", "Google"],
    "desc": (
        "Given an `m x n` character matrix `board` where each cell is either a battleship segment `'X'` or empty "
        "water `'.'`, return the number of battleships on `board`.\n\n"
        "Battleships are placed strictly horizontally (`1 x k`) or vertically (`k x 1`) for any length `k >= 1`, "
        "and there is at least one horizontal or vertical empty cell separating any two distinct battleships (no "
        "two ships touch orthogonally). Aim for a single-pass `O(1)` extra-space solution without modifying `board`."
    ),
    "cons": [
        "m == board.length",
        "n == board[i].length",
        "1 <= m, n <= 200",
        "board[i][j] is either '.' or 'X'.",
        "No two battleships are adjacent horizontally or vertically.",
    ],
    "hints": [
        "Every horizontal or vertical ship has a unique top-leftmost cell ('head') that has no 'X' immediately above it and no 'X' immediately to its left.",
        "Count all cells (r, c) where board[r][c] == 'X' and neither (r - 1, c) nor (r, c - 1) is 'X'.",
    ],
    "explanations": [
        "There is one 1x1 ship at (0, 0) and one vertical 3x1 ship in column 3, totaling 2 ships.",
        "An empty 1x1 board contains 0 battleships.",
        "Two horizontal ships and one vertical ship do not touch orthogonally, giving 3 battleships.",
    ],
    "time": "O(m * n)",
    "space": "O(1)",
    "method": "countBattleships",
    "params": [("board", "char[][]")],
    "ret": "int",
    "py": """        m, n = len(board), len(board[0])
        count = 0
        for r in range(m):
            for c in range(n):
                if board[r][c] == 'X':
                    if (r == 0 or board[r - 1][c] != 'X') and (c == 0 or board[r][c - 1] != 'X'):
                        count += 1
        return count""",
    "java": """        int m = board.length, n = board[0].length;
        int count = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (board[r][c] == 'X'
                        && (r == 0 || board[r - 1][c] != 'X')
                        && (c == 0 || board[r][c - 1] != 'X')) {
                    count++;
                }
            }
        }
        return count;""",
    "visible": [
        {"board": _grid_from_rows(["X..X", "...X", "...X"])},
        {"board": _grid_from_rows(["."])},
        {"board": _grid_from_rows(["XX.X", "...X", "XX.."])},
    ],
    "hidden": [
        {"board": _grid_from_rows(["X"])},
        {"board": _grid_from_rows(["XXXX"])},
        {"board": _grid_from_rows(["X", "X", "X", "X"])},
        {"board": _grid_from_rows(["X.X.X", ".X.X.", "X.X.X"])},
        {"board": _grid_from_rows([".....", ".....", "....."])},
        {"board": _grid_from_rows(["X.XX.", "X....", "..X.X", "..X.X"])},
        {"board": _battleships_grid(4701, 10, 10, 10)},
        {"board": _battleships_grid(4702, 20, 25, 30)},
        {"board": _battleships_grid(4703, 40, 40, 80)},
    ],
})

# ============================================================================
# Subtopic 5: Dynamic Grids (48 - 53)
# ============================================================================

TASKS.append({
    "slug": "48-range-addition-max-count",
    "title": "Range Addition Max Count",
    "difficulty": "Easy",
    "subtopic": "Dynamic Grids",
    "companies": ["Amazon", "Google", "LinkedIn"],
    "desc": (
        "You are given an `m x n` matrix initialized with all `0`s and a list of operations `ops`, where each "
        "`ops[i] = [ai, bi]` increments every cell `(r, c)` satisfying `0 <= r < ai` and `0 <= c < bi` by `1`.\n\n"
        "Count and return the number of cells in the matrix that contain the **maximum** value after applying all "
        "operations in `ops`."
    ),
    "cons": [
        "1 <= m, n <= 4 * 10^4",
        "0 <= ops.length <= 10^4",
        "ops[i].length == 2",
        "1 <= ops[i][0] <= m",
        "1 <= ops[i][1] <= n",
    ],
    "hints": [
        "Every operation covers a top-left rectangle [0..ai-1, 0..bi-1], so the cells incremented by ALL operations are precisely the intersection of all those rectangles.",
        "The intersection rectangle has dimensions min(ai) by min(bi) (or m by n if ops is empty), so the answer is simply minRow * minCol.",
    ],
    "explanations": [
        "The intersection of [0..1, 0..1] and [0..2, 0..2] is the 2x2 top-left submatrix (4 cells), each reaching value 2.",
        "The smallest ai is 2 and smallest bi is 2 across all operations, giving 2 * 2 = 4 maximum cells.",
        "With no operations, every cell holds the maximum value 0, so all 3 * 3 = 9 cells tie.",
    ],
    "time": "O(len(ops))",
    "space": "O(1)",
    "method": "maxCount",
    "params": [("m", "int"), ("n", "int"), ("ops", "int[][]")],
    "ret": "int",
    "py": """        min_r, min_c = m, n
        for a, b in ops:
            if a < min_r:
                min_r = a
            if b < min_c:
                min_c = b
        return min_r * min_c""",
    "java": """        int minR = m, minC = n;
        for (int[] op : ops) {
            if (op[0] < minR) minR = op[0];
            if (op[1] < minC) minC = op[1];
        }
        return minR * minC;""",
    "visible": [
        {"m": 3, "n": 3, "ops": [[2, 2], [3, 3]]},
        {"m": 3, "n": 3, "ops": [[2, 2], [3, 3], [3, 3], [3, 3], [2, 2], [3, 3], [3, 3], [3, 3], [2, 2], [3, 3], [3, 3], [3, 3]]},
        {"m": 3, "n": 3, "ops": []},
    ],
    "hidden": [
        {"m": 1, "n": 1, "ops": []},
        {"m": 1, "n": 1, "ops": [[1, 1]]},
        {"m": 40000, "n": 40000, "ops": []},
        {"m": 100, "n": 200, "ops": [[100, 1], [1, 200]]},
        {"m": 10, "n": 10, "ops": [[5, 8], [7, 4], [6, 6]]},
        {"m": 500, "n": 300, "ops": [[400, 250], [350, 200], [500, 100], [200, 300]]},
        {"m": 1000, "n": 1000, "ops": [[i, 1001 - i] for i in range(1, 50)]},
        {"m": 40000, "n": 40000, "ops": [[39999, 40000], [40000, 39999]]},
        {"m": 20000, "n": 30000, "ops": [[random.Random(4801 + i).randint(100, 20000), random.Random(4901 + i).randint(100, 30000)] for i in range(500)]},
    ],
})

TASKS.append({
    "slug": "49-increment-submatrices-by-one",
    "title": "Increment Submatrices by One",
    "difficulty": "Medium",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Amazon", "Meta", "Atlassian"],
    "desc": (
        "You are given a positive integer `n`, indicating an initially zero-filled `n x n` matrix `mat`, and a 2D "
        "array `queries` where each `queries[i] = [row1, col1, row2, col2]`.\n\n"
        "For every query, add `1` to every element in the inclusive rectangular submatrix with top-left corner "
        "`(row1, col1)` and bottom-right corner `(row2, col2)`.\n\n"
        "Return the resulting `n x n` matrix after performing all queries."
    ),
    "cons": [
        "1 <= n <= 100",
        "1 <= queries.length <= 10^4",
        "0 <= row1 <= row2 < n",
        "0 <= col1 <= col2 < n",
    ],
    "hints": [
        "Use a 2D difference array diff of size (n + 1) x (n + 1): for each query [r1, c1, r2, c2], add +1 at (r1, c1) and (r2 + 1, c2 + 1), and -1 at (r1, c2 + 1) and (r2 + 1, c1).",
        "Compute the 2D prefix sum of diff in O(n^2) time to recover the final matrix.",
    ],
    "explanations": [
        "Adding 1 to [1..2, 1..2] and [0..1, 0..1] overlaps at cell (1, 1), which ends up with value 2.",
        "Adding 1 to the entire 2x2 grid sets every entry to 1.",
        "Two identical queries on a 1x1 matrix increment the single cell to 2.",
    ],
    "time": "O(q + n^2)",
    "space": "O(n^2)",
    "method": "rangeAddQueries",
    "params": [("n", "int"), ("queries", "int[][]")],
    "ret": "int[][]",
    "py": """        diff = [[0] * (n + 1) for _ in range(n + 1)]
        for r1, c1, r2, c2 in queries:
            diff[r1][c1] += 1
            diff[r1][c2 + 1] -= 1
            diff[r2 + 1][c1] -= 1
            diff[r2 + 1][c2 + 1] += 1
        res = [[0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                v = diff[r][c]
                if r > 0:
                    v += res[r - 1][c]
                if c > 0:
                    v += res[r][c - 1]
                if r > 0 and c > 0:
                    v -= res[r - 1][c - 1]
                res[r][c] = v
        return res""",
    "java": """        int[][] diff = new int[n + 1][n + 1];
        for (int[] q : queries) {
            int r1 = q[0], c1 = q[1], r2 = q[2], c2 = q[3];
            diff[r1][c1] += 1;
            diff[r1][c2 + 1] -= 1;
            diff[r2 + 1][c1] -= 1;
            diff[r2 + 1][c2 + 1] += 1;
        }
        int[][] res = new int[n][n];
        for (int r = 0; r < n; r++) {
            for (int c = 0; c < n; c++) {
                int v = diff[r][c];
                if (r > 0) v += res[r - 1][c];
                if (c > 0) v += res[r][c - 1];
                if (r > 0 && c > 0) v -= res[r - 1][c - 1];
                res[r][c] = v;
            }
        }
        return res;""",
    "visible": [
        {"n": 3, "queries": [[1, 1, 2, 2], [0, 0, 1, 1]]},
        {"n": 2, "queries": [[0, 0, 1, 1]]},
        {"n": 1, "queries": [[0, 0, 0, 0], [0, 0, 0, 0]]},
    ],
    "hidden": [
        {"n": 1, "queries": [[0, 0, 0, 0]]},
        {"n": 3, "queries": [[0, 0, 0, 2], [2, 0, 2, 2], [0, 0, 2, 0], [0, 2, 2, 2]]},
        {"n": 4, "queries": [[0, 0, 3, 3], [1, 1, 2, 2], [1, 1, 2, 2]]},
        {"n": 4, "queries": [[0, 0, 0, 0], [1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3]]},
        {"n": 5, "queries": [[0, 0, 4, 0], [0, 4, 4, 4], [2, 0, 2, 4]]},
        {"n": 6, "queries": _rng_queries(4901, 6, 20)},
        {"n": 12, "queries": _rng_queries(4902, 12, 100)},
        {"n": 25, "queries": _rng_queries(4903, 25, 300)},
        {"n": 40, "queries": _rng_queries(4904, 40, 1000)},
    ],
})

TASKS.append({
    "slug": "50-count-unguarded-cells-in-grid",
    "title": "Count Unguarded Cells in the Grid",
    "difficulty": "Medium",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Amazon", "Meta", "Uber"],
    "desc": (
        "You are given two integers `m` and `n` representing an `m x n` grid, along with two 2D arrays `guards` "
        "and `walls` where `guards[i] = [r, c]` and `walls[j] = [r, c]` specify the distinct occupied positions of "
        "guards and walls.\n\n"
        "A guard can see every cell in the four cardinal directions (north, east, south, west) from its position "
        "unless obstructed by a wall or another guard. A cell is **guarded** if at least one guard can see it.\n\n"
        "Return the number of **unoccupied** cells in the grid that are **not** guarded."
    ),
    "cons": [
        "1 <= m, n <= 10^4",
        "2 <= m * n <= 10^5",
        "1 <= guards.length <= 5 * 10^4",
        "0 <= walls.length <= 5 * 10^4",
        "All positions in guards and walls are unique and within bounds.",
    ],
    "hints": [
        "Mark guards and walls on the grid (e.g., 1 = guard, 2 = wall), then ray-cast from every guard in all 4 directions stopping whenever you hit a wall, another guard, or the grid edge.",
        "Because a ray stops at another guard, each cell is visited at most twice horizontally and twice vertically, guaranteeing O(m * n) total time.",
    ],
    "explanations": [
        "In the 4x6 grid, 3 guards and 3 walls occupy 6 cells, and the guards watch 11 additional cells, leaving 7 unguarded empty cells.",
        "The single guard at (1, 1) is boxed in on all 4 sides by walls, so the 4 corner cells remain unguarded.",
        "One guard in a 1x5 strip with no walls sees all 4 other cells, leaving 0 unguarded cells.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "countUnguarded",
    "params": [("m", "int"), ("n", "int"), ("guards", "int[][]"), ("walls", "int[][]")],
    "ret": "int",
    "py": """        grid = [[0] * n for _ in range(m)]
        for r, c in guards:
            grid[r][c] = 1
        for r, c in walls:
            grid[r][c] = 2
        dirs = ((-1, 0), (1, 0), (0, -1), (0, 1))
        for r, c in guards:
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                while 0 <= nr < m and 0 <= nc < n:
                    cell = grid[nr][nc]
                    if cell == 1 or cell == 2:
                        break
                    grid[nr][nc] = 3
                    nr += dr
                    nc += dc
        ans = 0
        for row in grid:
            for v in row:
                if v == 0:
                    ans += 1
        return ans""",
    "java": """        int[][] grid = new int[m][n];
        for (int[] g : guards) grid[g[0]][g[1]] = 1;
        for (int[] w : walls) grid[w[0]][w[1]] = 2;
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};
        for (int[] g : guards) {
            for (int[] d : dirs) {
                int nr = g[0] + d[0], nc = g[1] + d[1];
                while (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                    int cell = grid[nr][nc];
                    if (cell == 1 || cell == 2) break;
                    grid[nr][nc] = 3;
                    nr += d[0];
                    nc += d[1];
                }
            }
        }
        int ans = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                if (grid[r][c] == 0) ans++;
            }
        }
        return ans;""",
    "visible": [
        {"m": 4, "n": 6, "guards": [[0, 0], [1, 1], [2, 3]], "walls": [[0, 1], [2, 2], [1, 4]]},
        {"m": 3, "n": 3, "guards": [[1, 1]], "walls": [[0, 1], [1, 0], [2, 1], [1, 2]]},
        {"m": 1, "n": 5, "guards": [[0, 2]], "walls": []},
    ],
    "hidden": [
        {"m": 2, "n": 1, "guards": [[0, 0]], "walls": [[1, 0]]},
        {"m": 2, "n": 2, "guards": [[0, 0]], "walls": []},
        {"m": 5, "n": 1, "guards": [[0, 0], [4, 0]], "walls": [[2, 0]]},
        {"m": 4, "n": 4, "guards": [[0, 0], [3, 3]], "walls": [[0, 3], [3, 0]]},
        {"m": 5, "n": 5, "guards": [[2, 2]], "walls": [[1, 1], [1, 3], [3, 1], [3, 3]]},
        {"m": 6, "n": 6, "guards": [[0, 0], [0, 1], [1, 0]], "walls": [[2, 2], [2, 3], [3, 2]]},
        {"m": 15, "n": 15, "guards": (gw50a := _rng_guards_walls(5001, 15, 15, 10, 25))[0], "walls": gw50a[1]},
        {"m": 40, "n": 40, "guards": (gw50b := _rng_guards_walls(5002, 40, 40, 40, 150))[0], "walls": gw50b[1]},
        {"m": 100, "n": 100, "guards": (gw50c := _rng_guards_walls(5003, 100, 100, 120, 400))[0], "walls": gw50c[1]},
    ],
})

TASKS.append({
    "slug": "51-largest-submatrix-with-rearrangements",
    "title": "Largest Submatrix With Rearrangements",
    "difficulty": "Medium",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Amazon", "Meta", "Microsoft"],
    "desc": (
        "You are given an `m x n` binary matrix `matrix` containing only `0`s and `1`s. You are allowed to rearrange "
        "the **columns** of `matrix` in any order.\n\n"
        "Return the area of the largest submatrix consisting entirely of `1`s that can be formed after optimally "
        "rearranging the columns."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m * n <= 10^5",
        "matrix[i][j] is either 0 or 1.",
    ],
    "hints": [
        "For each row r, maintain heights[c] = number of consecutive 1s ending at (r, c) moving upward in column c.",
        "Sorting heights in descending order simulates placing the tallest columns next to each other; check sortedHeights[i] * (i + 1) across all i.",
    ],
    "explanations": [
        "Moving column 2 next to column 0 creates a 2x2 all-ones submatrix of area 4 in the bottom two rows.",
        "Rearranging the single row puts all three 1s adjacent, forming a 1x3 submatrix of area 3.",
        "Only two 1s sit in the same row and no column has height 2, so the largest area is 2.",
    ],
    "time": "O(m * n * log n)",
    "space": "O(n)",
    "method": "largestSubmatrix",
    "params": [("matrix", "int[][]")],
    "ret": "int",
    "py": """        m, n = len(matrix), len(matrix[0])
        heights = [0] * n
        ans = 0
        for r in range(m):
            row = matrix[r]
            for c in range(n):
                heights[c] = heights[c] + 1 if row[c] == 1 else 0
            sorted_h = sorted(heights, reverse=True)
            for i, h in enumerate(sorted_h):
                if h == 0:
                    break
                area = h * (i + 1)
                if area > ans:
                    ans = area
        return ans""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        int[] heights = new int[n];
        int[] sorted = new int[n];
        int ans = 0;
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                heights[c] = matrix[r][c] == 1 ? heights[c] + 1 : 0;
                sorted[c] = heights[c];
            }
            Arrays.sort(sorted);
            for (int i = n - 1; i >= 0; i--) {
                int h = sorted[i];
                if (h == 0) break;
                int area = h * (n - i);
                if (area > ans) ans = area;
            }
        }
        return ans;""",
    "visible": [
        {"matrix": [[0, 0, 1], [1, 1, 1], [1, 0, 1]]},
        {"matrix": [[1, 0, 1, 0, 1]]},
        {"matrix": [[1, 1, 0], [1, 0, 1]]},
    ],
    "hidden": [
        {"matrix": [[0]]},
        {"matrix": [[1]]},
        {"matrix": [[0, 0], [0, 0]]},
        {"matrix": [[1, 1, 1], [1, 1, 1], [1, 1, 1]]},
        {"matrix": [[1], [1], [0], [1], [1], [1]]},
        {"matrix": [[1, 0, 0, 1], [1, 1, 0, 1], [0, 1, 1, 1], [1, 1, 1, 0]]},
        {"matrix": [[0, 1, 0, 1, 0], [1, 1, 1, 1, 0], [0, 1, 1, 1, 1], [1, 1, 0, 1, 1]]},
        {"matrix": _rng_bin_grid(5101, 20, 20, 0.7)},
        {"matrix": _rng_bin_grid(5102, 45, 45, 0.75)},
    ],
})

TASKS.append({
    "slug": "52-number-of-submatrices-that-sum-to-target",
    "title": "Number of Submatrices That Sum to Target",
    "difficulty": "Hard",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Meta", "Amazon", "Goldman Sachs", "Apple"],
    "desc": (
        "Given an `m x n` integer `matrix` and an integer `target`, return the number of non-empty rectangular "
        "submatrices whose elements sum to `target`.\n\n"
        "A submatrix `(r1, c1, r2, c2)` consists of all cells `(r, c)` with `r1 <= r <= r2` and `c1 <= c <= c2`. "
        "Two submatrices are distinct if they differ in any boundary coordinate."
    ),
    "cons": [
        "m == matrix.length",
        "n == matrix[i].length",
        "1 <= m, n <= 100",
        "-1000 <= matrix[i][j] <= 1000",
        "-10^8 <= target <= 10^8",
    ],
    "hints": [
        "Fix the top row r1 and bottom row r2 (or left/right columns if n < m), compressing each column into a single 1D sum.",
        "On the resulting 1D array, count subarrays summing to target in O(n) using a running prefix sum and a frequency hash map initialized with {0: 1}.",
    ],
    "explanations": [
        "Four 1x1 submatrices contain 0: the four corners of the 3x3 matrix.",
        "Five submatrices sum to 0: two 1x1 cells, two 1x2/2x1 pairs, and the entire 2x2 matrix.",
        "The single cell [904] does not equal target 0, so the count is 0.",
    ],
    "time": "O(min(m, n)^2 * max(m, n))",
    "space": "O(max(m, n))",
    "method": "numSubmatrixSumTarget",
    "params": [("matrix", "int[][]"), ("target", "int")],
    "ret": "int",
    "py": """        m, n = len(matrix), len(matrix[0])
        if m > n:
            matrix = [[matrix[r][c] for r in range(m)] for c in range(n)]
            m, n = n, m
        ans = 0
        for top in range(m):
            col_sums = [0] * n
            for bottom in range(top, m):
                row = matrix[bottom]
                freq = {0: 1}
                pref = 0
                for c in range(n):
                    col_sums[c] += row[c]
                    pref += col_sums[c]
                    ans += freq.get(pref - target, 0)
                    freq[pref] = freq.get(pref, 0) + 1
        return ans""",
    "java": """        int m = matrix.length, n = matrix[0].length;
        int[][] mat = matrix;
        if (m > n) {
            mat = new int[n][m];
            for (int r = 0; r < m; r++)
                for (int c = 0; c < n; c++)
                    mat[c][r] = matrix[r][c];
            int tmp = m; m = n; n = tmp;
        }
        int ans = 0;
        for (int top = 0; top < m; top++) {
            int[] colSums = new int[n];
            for (int bottom = top; bottom < m; bottom++) {
                int[] row = mat[bottom];
                Map<Integer, Integer> freq = new HashMap<>(n * 2);
                freq.put(0, 1);
                int pref = 0;
                for (int c = 0; c < n; c++) {
                    colSums[c] += row[c];
                    pref += colSums[c];
                    ans += freq.getOrDefault(pref - target, 0);
                    freq.put(pref, freq.getOrDefault(pref, 0) + 1);
                }
            }
        }
        return ans;""",
    "visible": [
        {"matrix": [[0, 1, 0], [1, 1, 1], [0, 1, 0]], "target": 0},
        {"matrix": [[1, -1], [-1, 1]], "target": 0},
        {"matrix": [[904]], "target": 0},
    ],
    "hidden": [
        {"matrix": [[5]], "target": 5},
        {"matrix": [[0, 0, 0], [0, 0, 0], [0, 0, 0]], "target": 0},
        {"matrix": [[1, 1, 1, 1]], "target": 2},
        {"matrix": [[1], [-1], [1], [-1]], "target": 0},
        {"matrix": [[1, 2, 3], [4, 5, 6], [7, 8, 9]], "target": 15},
        {"matrix": [[-1, 1, -1], [1, -1, 1], [-1, 1, -1]], "target": 0},
        {"matrix": [[10, -5, 5, -10], [5, 0, -5, 10], [-10, 5, 0, 5]], "target": 5},
        {"matrix": _rng_int_grid(5201, 15, 20, -5, 5), "target": 0},
        {"matrix": _rng_int_grid(5202, 30, 35, -10, 10), "target": 12},
    ],
})

TASKS.append({
    "slug": "53-stamping-the-grid",
    "title": "Stamping the Grid",
    "difficulty": "Hard",
    "subtopic": "Dynamic Grids",
    "companies": ["Google", "Amazon", "Meta", "Microsoft"],
    "desc": (
        "You are given an `m x n` binary matrix `grid` where `0` represents an empty cell and `1` represents an "
        "occupied cell. You also have an unlimited supply of rectangular stamps of fixed dimensions "
        "`stampHeight x stampWidth`.\n\n"
        "You want to place stamps on the grid subject to these rules:\n"
        "- Every empty (`0`) cell must be covered by at least one stamp.\n"
        "- No occupied (`1`) cell may be covered by any stamp.\n"
        "- Stamps may overlap each other, may not be rotated, and must lie completely inside the grid.\n\n"
        "Return `true` if it is possible to cover all empty cells, or `false` otherwise."
    ),
    "cons": [
        "m == grid.length",
        "n == grid[i].length",
        "1 <= m, n <= 10^4",
        "1 <= m * n <= 10^5",
        "grid[i][j] is either 0 or 1.",
        "1 <= stampHeight, stampWidth <= 10^5",
    ],
    "hints": [
        "Build a 2D prefix sum over grid so you can test in O(1) whether any stampHeight x stampWidth rectangle contains zero occupied cells.",
        "Whenever a stamp fits at top-left (r, c), greedily record it in a 2D difference array; after computing the 2D prefix sum of the difference array, verify every 0-cell has coverage > 0.",
    ],
    "explanations": [
        "Two overlapping 4x3 stamps cover the entire 5x3 region of empty cells without touching any occupied 1-cell.",
        "No 2x2 stamp can fit anywhere in the grid without overlapping an occupied cell, leaving empty cells uncovered.",
        "Every cell is already occupied (no empty cells exist), so the condition holds vacuously.",
    ],
    "time": "O(m * n)",
    "space": "O(m * n)",
    "method": "possibleToStamp",
    "params": [("grid", "int[][]"), ("stampHeight", "int"), ("stampWidth", "int")],
    "ret": "boolean",
    "py": """        m, n = len(grid), len(grid[0])
        h, w = stampHeight, stampWidth
        pref = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            row = grid[r]
            pr = pref[r]
            pr1 = pref[r + 1]
            for c in range(n):
                pr1[c + 1] = row[c] + pr[c + 1] + pr1[c] - pr[c]

        diff = [[0] * (n + 2) for _ in range(m + 2)]
        if h <= m and w <= n:
            for r in range(m - h + 1):
                r2 = r + h
                for c in range(n - w + 1):
                    c2 = c + w
                    if pref[r2][c2] - pref[r][c2] - pref[r2][c] + pref[r][c] == 0:
                        diff[r + 1][c + 1] += 1
                        diff[r2 + 1][c + 1] -= 1
                        diff[r + 1][c2 + 1] -= 1
                        diff[r2 + 1][c2 + 1] += 1

        for r in range(1, m + 1):
            dr = diff[r]
            dr_prev = diff[r - 1]
            row = grid[r - 1]
            for c in range(1, n + 1):
                dr[c] += dr_prev[c] + dr[c - 1] - dr_prev[c - 1]
                if row[c - 1] == 0 and dr[c] == 0:
                    return False
        return True""",
    "java": """        int m = grid.length, n = grid[0].length;
        int h = stampHeight, w = stampWidth;
        int[][] pref = new int[m + 1][n + 1];
        for (int r = 0; r < m; r++) {
            for (int c = 0; c < n; c++) {
                pref[r + 1][c + 1] = grid[r][c] + pref[r][c + 1] + pref[r + 1][c] - pref[r][c];
            }
        }
        int[][] diff = new int[m + 2][n + 2];
        if (h <= m && w <= n) {
            for (int r = 0; r <= m - h; r++) {
                int r2 = r + h;
                for (int c = 0; c <= n - w; c++) {
                    int c2 = c + w;
                    int sum = pref[r2][c2] - pref[r][c2] - pref[r2][c] + pref[r][c];
                    if (sum == 0) {
                        diff[r + 1][c + 1] += 1;
                        diff[r2 + 1][c + 1] -= 1;
                        diff[r + 1][c2 + 1] -= 1;
                        diff[r2 + 1][c2 + 1] += 1;
                    }
                }
            }
        }
        for (int r = 1; r <= m; r++) {
            for (int c = 1; c <= n; c++) {
                diff[r][c] += diff[r - 1][c] + diff[r][c - 1] - diff[r - 1][c - 1];
                if (grid[r - 1][c - 1] == 0 && diff[r][c] == 0) return false;
            }
        }
        return true;""",
    "visible": [
        {"grid": [[1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0], [1, 0, 0, 0]], "stampHeight": 4, "stampWidth": 3},
        {"grid": [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], "stampHeight": 2, "stampWidth": 2},
        {"grid": [[1, 1], [1, 1]], "stampHeight": 5, "stampWidth": 5},
    ],
    "hidden": [
        {"grid": [[0]], "stampHeight": 1, "stampWidth": 1},
        {"grid": [[0]], "stampHeight": 2, "stampWidth": 1},
        {"grid": [[0, 0, 0], [0, 0, 0]], "stampHeight": 2, "stampWidth": 2},
        {"grid": [[0, 0, 1], [0, 0, 0], [1, 0, 0]], "stampHeight": 2, "stampWidth": 2},
        {"grid": [[0, 0, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0]], "stampHeight": 1, "stampWidth": 2},
        {"grid": [[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]], "stampHeight": 2, "stampWidth": 2},
        {"grid": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], "stampHeight": 2, "stampWidth": 2},
        {"grid": _rng_stamp_grid(5301, 25, 25, 3, 4, feasible=True), "stampHeight": 3, "stampWidth": 4},
        {"grid": _rng_stamp_grid(5302, 35, 35, 4, 3, feasible=False), "stampHeight": 4, "stampWidth": 3},
    ],
})


def main() -> None:
    expected_prefixes = list(range(24, 54))
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

        params = [{"name": n, "type": t} for n, t in p["params"]]
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
            "signature": {
                "kind": "function",
                "method": p["method"],
                "params": params,
                "returns": p["ret"],
            },
        }
        (folder / "problem.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

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

        vis_code = repr([{"in": x} for x in p["visible"]])
        hid_code = repr([{"in": x} for x in p["hidden"]])
        (folder / "tests.py").write_text(
            f"def visible():\n    return {vis_code}\n\ndef hidden():\n    return {hid_code}\n",
            encoding="utf-8",
        )

    print(f"Generated {len(TASKS)} matrix problems (24-53) in {BASE}")


if __name__ == "__main__":
    main()
