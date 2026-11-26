class Solution:
    def subarrayBitwiseORs(self, arr: List[int]) -> int:
        ans = set()
        cur = set()
        for x in arr:
            cur = {x | y for y in cur}
            cur.add(x)
            ans.update(cur)
        return len(ans)
