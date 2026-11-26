class MinMaxSubarrayStack:
    def __init__(self):
        # Each entry: (val, cur_min, best_min, cur_max, best_max)
        self.st = []

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, val, val, val))
        else:
            _, p_cmin, p_bmin, p_cmax, p_bmax = self.st[-1]
            cmin = val if val < p_cmin + val else p_cmin + val
            bmin = cmin if cmin < p_bmin else p_bmin
            cmax = val if val > p_cmax + val else p_cmax + val
            bmax = cmax if cmax > p_bmax else p_bmax
            self.st.append((val, cmin, bmin, cmax, bmax))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMinSubarraySum(self) -> int:
        return self.st[-1][2]

    def getMaxSubarraySum(self) -> int:
        return self.st[-1][4]
