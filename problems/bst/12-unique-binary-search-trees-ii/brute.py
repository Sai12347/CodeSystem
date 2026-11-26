class Solution:
    def generateTrees(self, n: int) -> List[Optional[TreeNode]]:
        if n == 0:
            return []

        def build(lo: int, hi: int) -> List[Optional[TreeNode]]:
            if lo > hi:
                return [None]
            res = []
            for val in range(lo, hi + 1):
                for left in build(lo, val - 1):
                    for right in build(val + 1, hi):
                        res.append(TreeNode(val, left, right))
            return res

        return build(1, n)
