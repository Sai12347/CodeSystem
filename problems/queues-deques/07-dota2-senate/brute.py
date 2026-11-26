class Solution:
    def predictPartyVictory(self, senate: str) -> str:
        active = list(senate)
        ban_r = 0
        ban_d = 0
        while True:
            has_r = False
            has_d = False
            nxt = []
            for ch in active:
                if ch == 'R':
                    if ban_r > 0:
                        ban_r -= 1
                    else:
                        has_r = True
                        ban_d += 1
                        nxt.append('R')
                else:
                    if ban_d > 0:
                        ban_d -= 1
                    else:
                        has_d = True
                        ban_r += 1
                        nxt.append('D')
            if not has_r:
                return "Dire"
            if not has_d:
                return "Radiant"
            active = nxt
