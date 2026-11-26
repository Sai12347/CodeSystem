class GcdStack:
    def __init__(self):
        self.vals = []
        self.gcds = []

    def push(self, val: int) -> None:
        import math
        self.vals.append(val)
        if not self.gcds:
            self.gcds.append(val)
        else:
            self.gcds.append(math.gcd(self.gcds[-1], val))

    def pop(self) -> None:
        self.vals.pop()
        self.gcds.pop()

    def top(self) -> int:
        return self.vals[-1]

    def getGcd(self) -> int:
        return self.gcds[-1]
