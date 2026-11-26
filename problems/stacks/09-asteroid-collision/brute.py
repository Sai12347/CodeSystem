class Solution:
    def asteroidCollision(self, asteroids: List[int]) -> List[int]:
        # Repeatedly resolve all adjacent (positive, negative) collisions per pass.
        cur = list(asteroids)
        while True:
            nxt = []
            i = 0
            n = len(cur)
            changed = False
            while i < n:
                if i + 1 < n and cur[i] > 0 and cur[i + 1] < 0:
                    changed = True
                    if cur[i] > -cur[i + 1]:
                        nxt.append(cur[i])
                    elif cur[i] < -cur[i + 1]:
                        nxt.append(cur[i + 1])
                    i += 2
                else:
                    nxt.append(cur[i])
                    i += 1
            if not changed:
                return nxt
            cur = nxt
