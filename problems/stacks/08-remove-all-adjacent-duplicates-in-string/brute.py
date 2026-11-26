class Solution:
    def removeDuplicates(self, s: str) -> str:
        # Repeatedly remove all non-overlapping adjacent duplicate pairs per pass.
        cur = list(s)
        while True:
            nxt = []
            i = 0
            n = len(cur)
            changed = False
            while i < n:
                if i + 1 < n and cur[i] == cur[i + 1]:
                    i += 2
                    changed = True
                else:
                    nxt.append(cur[i])
                    i += 1
            if not changed:
                return "".join(nxt)
            cur = nxt
