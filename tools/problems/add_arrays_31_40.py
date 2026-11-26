import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "arrays"
tasks = [
    {
        "slug": "31-maximum-circular-subarray-sum", "title": "Maximum Circular Subarray Sum", "difficulty": "Medium", "subtopic": "Subarrays", "method": "maxCircularSubarraySum", "ret": "int",
        "description": "Given a non-empty integer array `nums` arranged in a circle, return the largest sum of a non-empty contiguous segment. A segment may wrap from the last element to the first, but it may contain each array position at most once. Input: `nums`. Output: the maximum segment sum.",
        "constraints": ["1 <= nums.length <= 100000", "-10000 <= nums[i] <= 10000"], "time": "O(n)", "space": "O(1)",
        "py": "        total = sum(nums)\n        max_end = min_end = max_sum = min_sum = nums[0]\n        for x in nums[1:]:\n            max_end = max(x, max_end + x)\n            max_sum = max(max_sum, max_end)\n            min_end = min(x, min_end + x)\n            min_sum = min(min_sum, min_end)\n        return max_sum if max_sum < 0 else max(max_sum, total - min_sum)",
        "java": "        int total = 0, maxEnd = nums[0], minEnd = nums[0], maxSum = nums[0], minSum = nums[0];\n        total = nums[0];\n        for (int i = 1; i < nums.length; i++) { int x = nums[i]; total += x; maxEnd = Math.max(x, maxEnd + x); maxSum = Math.max(maxSum, maxEnd); minEnd = Math.min(x, minEnd + x); minSum = Math.min(minSum, minEnd); }\n        return maxSum < 0 ? maxSum : Math.max(maxSum, total - minSum);",
        "examples": [([5, -3, 5], 10), ([1, -2, 3, -2], 3)], "tests": [[5,-3,5],[1,-2,3,-2],[-3,-2,-3],[7],[0,0,0],[8,-1,2,-6,7],[4,-5,4],[-1,5,-2,5],[-8,3,-7,4,2]]
    },
    {
        "slug": "32-leftmost-equilibrium-position", "title": "Leftmost Equilibrium Position", "difficulty": "Easy", "subtopic": "Prefix/Suffix", "method": "equilibriumIndex", "ret": "int",
        "description": "Given an integer array `nums`, find the smallest index whose elements strictly before it sum to the elements strictly after it. The element at the index is excluded from both sums. Return -1 if no such index exists. Input: `nums`. Output: the leftmost matching index or -1.",
        "constraints": ["1 <= nums.length <= 100000", "-100000 <= nums[i] <= 100000"], "time": "O(n)", "space": "O(1)",
        "py": "        right = sum(nums)\n        left = 0\n        for i, x in enumerate(nums):\n            right -= x\n            if left == right:\n                return i\n            left += x\n        return -1",
        "java": "        long right = 0, left = 0;\n        for (int x : nums) right += x;\n        for (int i = 0; i < nums.length; i++) { right -= nums[i]; if (left == right) return i; left += nums[i]; }\n        return -1;",
        "examples": [([1, 7, 3, 6, 5, 6], 3), ([1, 2, 3], -1)], "tests": [[1,7,3,6,5,6],[1,2,3],[0],[2,-2,0],[0,0,0],[-1,1],[-7,1,5,2,-4,3,0],[4,-2,-2],[3,1,-1,1,-4]]
    },
    {
        "slug": "33-dominant-value-index", "title": "Dominant Value Index", "difficulty": "Easy", "subtopic": "Traversal", "method": "dominantIndex", "ret": "int",
        "description": "Given a non-empty array of non-negative integers, return the index of its largest value if that value is at least twice every other value. If the largest value is tied with another value, it is dominant only when both are zero. Return -1 when no dominant index exists. Input: `nums`. Output: the qualifying index or -1.",
        "constraints": ["1 <= nums.length <= 100000", "0 <= nums[i] <= 1000000"], "time": "O(n)", "space": "O(1)",
        "py": "        best = second = -1\n        index = -1\n        for i, x in enumerate(nums):\n            if x > best:\n                second, best, index = best, x, i\n            elif x > second:\n                second = x\n        return index if best >= 2 * second else -1",
        "java": "        int best = -1, second = -1, index = -1;\n        for (int i = 0; i < nums.length; i++) { int x = nums[i]; if (x > best) { second = best; best = x; index = i; } else if (x > second) second = x; }\n        return best >= 2L * second ? index : -1;",
        "examples": [([3, 6, 1, 0], 1), ([1, 2, 3, 4], -1)], "tests": [[3,6,1,0],[1,2,3,4],[5],[0,0],[0,0,0],[1,0,0],[1,1],[10,2,5,1],[1000000,500000,0]]
    },
    {
        "slug": "34-longest-run-of-ones", "title": "Longest Run of Ones", "difficulty": "Easy", "subtopic": "Traversal", "method": "longestRunOfOnes", "ret": "int",
        "description": "Given a non-empty binary array `nums`, return the length of its longest contiguous run of ones. Zeros end a run. Input: `nums`, whose values are only 0 or 1. Output: the maximum run length, or 0 when there are no ones.",
        "constraints": ["1 <= nums.length <= 100000", "nums[i] is either 0 or 1"], "time": "O(n)", "space": "O(1)",
        "py": "        best = run = 0\n        for x in nums:\n            run = run + 1 if x == 1 else 0\n            best = max(best, run)\n        return best",
        "java": "        int best = 0, run = 0;\n        for (int x : nums) { run = x == 1 ? run + 1 : 0; best = Math.max(best, run); }\n        return best;",
        "examples": [([1, 1, 0, 1, 1, 1], 3), ([0, 0, 0], 0)], "tests": [[1,1,0,1,1,1],[0,0,0],[1],[1,1,1,1],[0,1,0,1,0],[1,0,1,1,0,1],[0,1,1,0,1,1,1,0],[1,0,0,1,1]]
    },
    {
        "slug": "35-minimum-distance-between-equal-values", "title": "Minimum Distance Between Equal Values", "difficulty": "Easy", "subtopic": "Traversal", "method": "minimumEqualDistance", "ret": "int",
        "description": "Given an integer array `nums`, find the smallest positive distance `j - i` among pairs of indices `i < j` with `nums[i] == nums[j]`. Return -1 if every value occurs only once. Input: `nums`. Output: the minimum distance or -1.",
        "constraints": ["1 <= nums.length <= 100000", "-1000000000 <= nums[i] <= 1000000000"], "time": "O(n)", "space": "O(n)",
        "py": "        last = {}\n        best = len(nums) + 1\n        for i, x in enumerate(nums):\n            if x in last:\n                best = min(best, i - last[x])\n            last[x] = i\n        return best if best <= len(nums) else -1",
        "java": "        Map<Integer, Integer> last = new HashMap<>();\n        int best = nums.length + 1;\n        for (int i = 0; i < nums.length; i++) { Integer prev = last.put(nums[i], i); if (prev != null) best = Math.min(best, i - prev); }\n        return best <= nums.length ? best : -1;",
        "examples": [([7, 1, 3, 4, 1, 7], 3), ([1, 2, 3], -1)], "tests": [[7,1,3,4,1,7],[1,2,3],[-5,-5],[1,2,1,1],[0,1,2,3,0],[4,5,4,5],[9,8,7,6,5],[1,2,3,1,2,3]]
    },
    {
        "slug": "36-longest-strictly-increasing-run", "title": "Longest Strictly Increasing Run", "difficulty": "Easy", "subtopic": "Traversal", "method": "longestIncreasingRun", "ret": "int",
        "description": "Given a non-empty integer array `nums`, return the length of its longest contiguous strictly increasing run. A run is contiguous, and each next value must be greater than the previous value. Input: `nums`. Output: the maximum run length.",
        "constraints": ["1 <= nums.length <= 100000", "-1000000000 <= nums[i] <= 1000000000"], "time": "O(n)", "space": "O(1)",
        "py": "        best = run = 1\n        for i in range(1, len(nums)):\n            run = run + 1 if nums[i] > nums[i - 1] else 1\n            best = max(best, run)\n        return best",
        "java": "        int best = 1, run = 1;\n        for (int i = 1; i < nums.length; i++) { run = nums[i] > nums[i - 1] ? run + 1 : 1; best = Math.max(best, run); }\n        return best;",
        "examples": [([1, 3, 5, 4, 7], 3), ([2, 2, 2], 1)], "tests": [[1,3,5,4,7],[2,2,2],[1],[1,2,3,4,5],[-3,-2,-1,0],[5,4,3,2],[1,3,2,4,5,0,1,2],[7,9,8,10,11]]
    },
    {
        "slug": "37-longest-strictly-decreasing-run", "title": "Longest Strictly Decreasing Run", "difficulty": "Easy", "subtopic": "Traversal", "method": "longestDecreasingRun", "ret": "int",
        "description": "Given a non-empty integer array `nums`, return the length of its longest contiguous strictly decreasing run. A run is contiguous, and each next value must be smaller than the previous value. Input: `nums`. Output: the maximum run length.",
        "constraints": ["1 <= nums.length <= 100000", "-1000000000 <= nums[i] <= 1000000000"], "time": "O(n)", "space": "O(1)",
        "py": "        best = run = 1\n        for i in range(1, len(nums)):\n            run = run + 1 if nums[i] < nums[i - 1] else 1\n            best = max(best, run)\n        return best",
        "java": "        int best = 1, run = 1;\n        for (int i = 1; i < nums.length; i++) { run = nums[i] < nums[i - 1] ? run + 1 : 1; best = Math.max(best, run); }\n        return best;",
        "examples": [([9, 7, 4, 5, 3], 3), ([2, 2, 2], 1)], "tests": [[9,7,4,5,3],[2,2,2],[1],[5,4,3,2,1],[-1,-2,-3,-4],[1,2,3],[8,6,7,5,4,3,9],[0,-1,0,-1,-2]]
    },
    {
        "slug": "38-count-record-breakers", "title": "Count Record Breakers", "difficulty": "Easy", "subtopic": "Traversal", "method": "countRecordBreakers", "ret": "int",
        "description": "Scan an integer array from left to right. The first element is a record breaker; each later element is a record breaker only when it is strictly greater than every earlier element. Return the number of record breakers. Input: a non-empty array `nums`. Output: the count.",
        "constraints": ["1 <= nums.length <= 100000", "-1000000000 <= nums[i] <= 1000000000"], "time": "O(n)", "space": "O(1)",
        "py": "        count = 0\n        high = None\n        for x in nums:\n            if high is None or x > high:\n                count += 1\n                high = x\n        return count",
        "java": "        int count = 0, high = 0; boolean seen = false;\n        for (int x : nums) if (!seen || x > high) { count++; high = x; seen = true; }\n        return count;",
        "examples": [([5, 1, 6, 7, 2], 3), ([4, 4, 4], 1)], "tests": [[5,1,6,7,2],[4,4,4],[1],[1,2,3,4],[4,3,2,1],[-5,-2,-3,-1],[0,0,1,0,2],[3,8,8,9]]
    },
    {
        "slug": "39-strict-local-peak-count", "title": "Strict Local Peak Count", "difficulty": "Easy", "subtopic": "Traversal", "method": "countStrictPeaks", "ret": "int",
        "description": "A strict local peak is an interior array element that is greater than both immediate neighbors. Given an integer array `nums`, return the number of strict local peaks. The first and last elements are never peaks. Input: `nums`. Output: the peak count.",
        "constraints": ["3 <= nums.length <= 100000", "-1000000000 <= nums[i] <= 1000000000"], "time": "O(n)", "space": "O(1)",
        "py": "        return sum(1 for i in range(1, len(nums) - 1) if nums[i] > nums[i - 1] and nums[i] > nums[i + 1])",
        "java": "        int count = 0;\n        for (int i = 1; i + 1 < nums.length; i++) if (nums[i] > nums[i - 1] && nums[i] > nums[i + 1]) count++;\n        return count;",
        "examples": [([1, 3, 2, 4, 1], 2), ([1, 2, 3], 0)], "tests": [[1,3,2,4,1],[1,2,3],[3,1,3],[5,4,3,2],[0,2,0,2,0,2,0],[1,1,1],[9,1,8,2,7,3,6],[0,-1,0]]
    },
    {
        "slug": "40-maximum-adjacent-pair-product", "title": "Maximum Adjacent Pair Product", "difficulty": "Easy", "subtopic": "Traversal", "method": "maximumAdjacentProduct", "ret": "int",
        "description": "Given an integer array `nums` with at least two elements, choose two neighboring positions and return the largest product of their values. Products may be negative or zero. Input: `nums`. Output: the maximum adjacent pair product.",
        "constraints": ["2 <= nums.length <= 100000", "-10000 <= nums[i] <= 10000"], "time": "O(n)", "space": "O(1)",
        "py": "        best = nums[0] * nums[1]\n        for i in range(1, len(nums) - 1):\n            best = max(best, nums[i] * nums[i + 1])\n        return best",
        "java": "        int best = nums[0] * nums[1];\n        for (int i = 1; i + 1 < nums.length; i++) best = Math.max(best, nums[i] * nums[i + 1]);\n        return best;",
        "examples": [([1, 5, 3, 2], 15), ([-5, -2, 4], 10)], "tests": [[1,5,3,2],[-5,-2,4],[1,1],[0,9,0],[3,-4,-5,2],[-1,2,-3,4],[100,-100,100],[-10,-10,-10]]
    },
]

topics = {t["id"]: t for t in json.loads((ROOT / "problems" / "topics.json").read_text())}
roster_path = ROOT / "problems" / "roster.json"
roster = json.loads(roster_path.read_text())
for p in tasks:
    folder = BASE / p["slug"]
    folder.mkdir()
    meta = {
        "title": p["title"], "difficulty": p["difficulty"], "subtopic": p["subtopic"],
        "companies": ["Amazon", "Microsoft", "Google"], "description": p["description"],
        "constraints": p["constraints"], "hints": ["Scan the array while retaining only the state needed for the answer.", "Check the first, last, repeated, and all-equal cases."],
        "examples": [{"input": f"nums = {arr}", "output": str(out)} for arr, out in p["examples"]],
        "timeComplexity": p["time"], "spaceComplexity": p["space"], "compare": "exact",
        "signature": {"kind": "function", "method": p["method"], "params": [{"name": "nums", "type": "int[]"}], "returns": p["ret"]}
    }
    (folder / "problem.json").write_text(json.dumps(meta, indent=2) + "\n")
    (folder / "solution.py").write_text("class Solution:\n    def " + p["method"] + "(self, nums: List[int]) -> int:\n" + p["py"] + "\n")
    (folder / "Solution.java").write_text("class Solution {\n    public int " + p["method"] + "(int[] nums) {\n" + p["java"] + "\n    }\n}\n")
    cases = p["tests"]
    test_src = "def visible():\n    return " + repr([{"in": {"nums": a}} for a in cases[:3]]) + "\n\ndef hidden():\n    return " + repr([{"in": {"nums": a}} for a in cases[3:]]) + "\n"
    (folder / "tests.py").write_text(test_src)
    roster.setdefault("arrays", []).append([p["slug"], p["title"], p["difficulty"], p["subtopic"], None])
roster_path.write_text(json.dumps(roster, indent=2) + "\n")
print(f"Created {len(tasks)} array questions")
