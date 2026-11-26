class TopKMinStack:
    def __init__(self):
        self.up = []
        self.pref_min = []

    def push(self, val: int) -> None:
        idx = len(self.up)
        row = [val]
        j = 1
        while (1 << j) <= idx + 1:
            prev = self.up[idx - (1 << (j - 1))][j - 1]
            cur = row[j - 1]
            row.append(cur if cur < prev else prev)
            j += 1
        self.up.append(row)
        self.pref_min.append(val if not self.pref_min or val < self.pref_min[-1] else self.pref_min[-1])

    def pop(self) -> int:
        self.pref_min.pop()
        return self.up.pop()[0]

    def getMin(self) -> int:
        return self.pref_min[-1]

    def getTopKMin(self, k: int) -> int:
        n = len(self.up)
        p = k.bit_length() - 1
        a = self.up[n - 1][p]
        b = self.up[n - k + (1 << p) - 1][p]
        return a if a < b else b
