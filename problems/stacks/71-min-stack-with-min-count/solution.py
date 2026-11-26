class CountMinStack:
    def __init__(self):
        self.st = []  # (val, min_val, min_cnt)

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, 1))
        else:
            _, mn, cnt = self.st[-1]
            if val < mn:
                self.st.append((val, val, 1))
            elif val == mn:
                self.st.append((val, mn, cnt + 1))
            else:
                self.st.append((val, mn, cnt))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]

    def getMinCount(self) -> int:
        return self.st[-1][2]
