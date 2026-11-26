class RunLengthMinStack:
    def __init__(self):
        self.runs = []  # [val, count, running_min]

    def pushMany(self, val: int, count: int) -> None:
        if self.runs and self.runs[-1][0] == val:
            self.runs[-1][1] += count
        else:
            mn = val if not self.runs or val < self.runs[-1][2] else self.runs[-1][2]
            self.runs.append([val, count, mn])

    def popMany(self, count: int) -> int:
        total = 0
        rem = count
        while rem > 0:
            entry = self.runs[-1]
            if entry[1] <= rem:
                total += entry[0] * entry[1]
                rem -= entry[1]
                self.runs.pop()
            else:
                total += entry[0] * rem
                entry[1] -= rem
                rem = 0
        return total

    def top(self) -> int:
        return self.runs[-1][0]

    def getMin(self) -> int:
        return self.runs[-1][2]
