# CodeSystem Problem Authoring Specification

Every problem lives in its own folder under `problems/<topicId>/<NN>-<slug>/` where `<NN>` is a two-digit sequence number (`01`, `02`, ...) and `<slug>` is globally unique kebab-case (`two-sum`, `lru-cache`, etc.).

## Files in Each Problem Folder

1. `problem.json` — problem metadata & signature
2. `tests.py` — defines `visible()` (2-3 tests) and `hidden()` (8-12 tests)
3. `solution.py` — optimal reference solution in Python 3.10+
4. `Solution.java` — optimal reference solution in Java 21
5. `brute.py` *(optional, strongly recommended for non-trivial problems)* — simple brute-force Python solution used to cross-check expected outputs on smaller tests
6. `adapter.py`, `Adapter.java`, `starter.py`, `starter.java` *(only when `signature.kind == "adapter"`)*

## `problem.json` Schema

```json
{
  "title": "Two Sum",
  "difficulty": "Easy",
  "subtopic": "Hash Tables",
  "companies": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
  "leetcode": 1,
  "description": "Full, unambiguous problem statement with exact input/output definitions, edge-case rules, and tie-breaking rules.",
  "constraints": [
    "2 <= nums.length <= 10^4",
    "-10^9 <= nums[i] <= 10^9",
    "-10^9 <= target <= 10^9",
    "Only one valid answer exists."
  ],
  "hints": [
    "Think about what information you need as you scan the array from left to right.",
    "A hash map lets you check in O(1) average time whether target - nums[i] has already been seen."
  ],
  "examples": [
    {"explanation": "Because nums[0] + nums[1] == 9, we return [0, 1]."},
    {"explanation": "nums[1] + nums[2] == 6, so return [1, 2]."}
  ],
  "timeComplexity": "O(n)",
  "spaceComplexity": "O(n)",
  "compare": "exact",
  "signature": {
    "kind": "function",
    "method": "twoSum",
    "params": [
      {"name": "nums", "type": "int[]"},
      {"name": "target", "type": "int"}
    ],
    "returns": "int[]"
  }
}
```

### Allowed Values
- `difficulty`: `"Easy"`, `"Medium"`, or `"Hard"` (accurate, real difficulty — no arbitrary modulo)
- `subtopic`: MUST be one of the `subtopics` listed for this topic in `problems/topics.json`
- `companies`: non-empty list chosen from `["Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Uber", "Goldman Sachs", "Adobe", "Atlassian", "Salesforce", "Oracle", "Bloomberg", "LinkedIn"]`
- `compare`:
  - `"exact"` (default): exact JSON equality
  - `"float"`: numeric tolerance `1e-5`
  - `"sorted"`: top-level list order does not matter (e.g., pair of indices, list of valid strings, subsets of scalars)
  - `"sortedDeep"`: nested list order does not matter at any level (e.g., `3Sum`, `Group Anagrams`, `Subsets`, `Combinations`)
  - `"anyOf"`: every test in `tests.py` provides `"out": [validAnswer1, validAnswer2, ...]`
- `signature`:
  - `kind: "function"`:
    - `method`: camelCase method name inside `class Solution` (same name in both Java and Python!)
    - `params`: list of `{"name": "...", "type": "..."}`
    - `returns`: type string or `"void"`
    - `output` *(optional)*: `{"mode": "return"}` (default), `{"mode": "param", "param": "nums"}` (for void in-place mutations like reverse/sort/rotate), or `{"mode": "prefix", "param": "nums"}` (returns int `k`, compares `nums[:k]` like Remove Duplicates / Remove Element).
  - `kind: "design"`:
    - `className`: PascalCase class name (e.g. `"LRUCache"`, `"Trie"`, `"MinStack"`)
    - `constructor`: `{"params": [...]}`
    - `methods`: list of `{"name": "...", "params": [...], "returns": "..."}`
    - Every test input has `{"ops": ["ClassName", "op1", ...], "args": [[ctorArgs], [op1Args], ...]}`.
  - `kind: "adapter"`:
    - Used for graph/cyclic-linked-list/special-node problems (e.g. `Linked List Cycle`, `Intersection of Two Linked Lists`, `Clone Graph`, `Copy List with Random Pointer`, `Populating Next Right Pointers`, `Flatten a Multilevel Doubly Linked List`, `Lowest Common Ancestor` where nodes are specified by values).
    - Must provide `inputs` in `signature` for display, plus `adapter.py`, `Adapter.java`, `starter.py`, `starter.java`.

### Supported Types (Java spelling, auto-mapped to Python)
`int`, `long`, `double`, `boolean`, `char`, `String`, `Integer`, `Long`, `Double`, `Boolean`, `Character`, `ListNode`, `TreeNode`, `T[]`, `T[][]`, `List<T>`, `List<List<T>>`.

## `tests.py` Rules
- Must define `visible()` returning 2 or 3 dicts `{"in": {...}}` and `hidden()` returning 8 to 12 dicts `{"in": {...}}`.
- Do NOT hand-compute `"out"` unless `compare == "anyOf"` or you specifically want to assert a known value; `build.py` computes expected outputs from `solution.py` and verifies `Solution.java` (and `brute.py` if present) match on every test!
- Hidden tests MUST cover:
  - Minimum / empty / single-element boundaries
  - Duplicates, all-equal, already-sorted, reverse-sorted
  - Negative numbers / zeros / integer overflow boundaries (where allowed by constraints)
  - Tricky algorithmic edge cases specific to the problem (disconnected graphs, cycles, unreachable targets, tie cases, degenerate skewed trees)
  - 1-2 larger performance/stress tests (staying within the 64 KB per-test and 200 KB total JSON size limits — e.g. `n = 1000..5000` for O(n)/O(n log n) problems, keeping inputs deterministic with fixed `random.Random(seed)`!).
- No duplicate test inputs across visible + hidden.
- Every test input MUST strictly satisfy the problem's stated `constraints`!

## Code Rules
- `solution.py`: `class Solution:` (or `class <ClassName>:` for design). Common typing & stdlib (`List`, `Optional`, `deque`, `defaultdict`, `Counter`, `heapq`, `bisect`, `math`, `lru_cache`, `ListNode`, `TreeNode`) are auto-imported by the judge prelude.
- `Solution.java`: `class Solution { ... }` (or `class <ClassName> { ... }` for design). `java.util.*`, `java.util.function.*`, `java.util.stream.*`, `java.math.*`, `ListNode`, `TreeNode` are auto-available. Do not use `package` statements.
- Method names MUST match `signature.method` identically in Java and Python (camelCase).
- Solutions MUST be genuinely optimal (matching stated `timeComplexity` & `spaceComplexity`) and bug-free on all edge cases.
