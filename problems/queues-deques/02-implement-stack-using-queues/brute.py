class MyStack:
    def __init__(self):
        self.st = []

    def push(self, x: int) -> None:
        self.st.append(x)

    def pop(self) -> int:
        return self.st.pop()

    def top(self) -> int:
        return self.st[-1]

    def empty(self) -> bool:
        return len(self.st) == 0
