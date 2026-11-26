class MinQueue:
    def __init__(self):
        self.in_st = []
        self.out_st = []

    def _pour(self) -> None:
        if not self.out_st:
            while self.in_st:
                val, _ = self.in_st.pop()
                mn = val if not self.out_st or val < self.out_st[-1][1] else self.out_st[-1][1]
                self.out_st.append((val, mn))

    def enqueue(self, val: int) -> None:
        mn = val if not self.in_st or val < self.in_st[-1][1] else self.in_st[-1][1]
        self.in_st.append((val, mn))

    def dequeue(self) -> int:
        self._pour()
        return self.out_st.pop()[0]

    def front(self) -> int:
        self._pour()
        return self.out_st[-1][0]

    def getMin(self) -> int:
        if not self.in_st:
            return self.out_st[-1][1]
        if not self.out_st:
            return self.in_st[-1][1]
        return min(self.in_st[-1][1], self.out_st[-1][1])
