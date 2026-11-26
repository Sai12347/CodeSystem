class Solution:
    def canBeValid(self, s: str, locked: str) -> bool:
        n = len(s)
        if n % 2 == 1:
            return False
        open_locked = []
        unlocked = []
        for i in range(n):
            if locked[i] == '0':
                unlocked.append(i)
            elif s[i] == '(':
                open_locked.append(i)
            else:
                if open_locked:
                    open_locked.pop()
                elif unlocked:
                    unlocked.pop()
                else:
                    return False
        while open_locked and unlocked and open_locked[-1] < unlocked[-1]:
            open_locked.pop()
            unlocked.pop()
        return not open_locked
