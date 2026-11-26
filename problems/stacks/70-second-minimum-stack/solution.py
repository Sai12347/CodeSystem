class SecondMinStack:
    def __init__(self):
        self.st = []  # (val, min1, min2)

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, 10**18))
        else:
            _, m1, m2 = self.st[-1]
            if val < m1:
                self.st.append((val, val, m1))
            elif val < m2:
                self.st.append((val, m1, val))
            else:
                self.st.append((val, m1, m2))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]

    def getSecondMin(self) -> int:
        return self.st[-1][2]
