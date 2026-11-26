class RangeStack:
    def __init__(self):
        self.st = []

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, val))
        else:
            _, mn, mx = self.st[-1]
            self.st.append((val, val if val < mn else mn, val if val > mx else mx))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getRange(self) -> int:
        _, mn, mx = self.st[-1]
        return mx - mn
