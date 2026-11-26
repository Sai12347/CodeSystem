class Solution:
    def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        if n == 0:
            return []

        @lru_cache(maxsize=None)
        def build(lo: int, hi: int) -> tuple:
            if lo > hi:
                return (None,)
            trees = []
            for val in range(lo, hi + 1):
                for left in build(lo, val - 1):
                    for right in build(val + 1, hi):
                        trees.append(TreeNode(val, left, right))
            return tuple(trees)

        return list(build(1, n))
