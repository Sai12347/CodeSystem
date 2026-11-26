from collections import deque


class SnakeGame:
    def __init__(self, width: int, height: int, food: List[List[int]]):
        self.w = width
        self.h = height
        self.food = food
        self.fi = 0
        self.body: deque[tuple[int, int]] = deque([(0, 0)])
        self.occupied: set[tuple[int, int]] = {(0, 0)}
        self.over = False

    def move(self, direction: str) -> int:
        if self.over:
            return -1
        r, c = self.body[0]
        if direction == "U":
            r -= 1
        elif direction == "D":
            r += 1
        elif direction == "L":
            c -= 1
        else:
            c += 1
        if r < 0 or r >= self.h or c < 0 or c >= self.w:
            self.over = True
            return -1
        eating = self.fi < len(self.food) and self.food[self.fi][0] == r and self.food[self.fi][1] == c
        if not eating:
            tail = self.body.pop()
            self.occupied.remove(tail)
        if (r, c) in self.occupied:
            self.over = True
            return -1
        self.body.appendleft((r, c))
        self.occupied.add((r, c))
        if eating:
            self.fi += 1
        return len(self.body) - 1
