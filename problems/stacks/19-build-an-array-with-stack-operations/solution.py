class Solution:
    def buildArray(self, target: List[int], n: int) -> List[str]:
        ops = []
        cur = 1
        for val in target:
            while cur < val:
                ops.append("Push")
                ops.append("Pop")
                cur += 1
            ops.append("Push")
            cur += 1
        return ops
