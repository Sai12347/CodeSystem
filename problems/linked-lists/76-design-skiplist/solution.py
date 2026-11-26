import random


class _SkipNode:
    __slots__ = ("val", "forward")

    def __init__(self, val: int, level: int):
        self.val = val
        self.forward: list[_SkipNode | None] = [None] * level


class Skiplist:
    MAX_LEVEL = 16

    def __init__(self):
        self.head = _SkipNode(-10**9, self.MAX_LEVEL)
        self.level = 1
        self.rng = random.Random(42)

    def _random_level(self) -> int:
        lvl = 1
        while lvl < self.MAX_LEVEL and self.rng.getrandbits(1):
            lvl += 1
        return lvl

    def search(self, target: int) -> bool:
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].val < target:
                curr = curr.forward[i]
        cand = curr.forward[0]
        return cand is not None and cand.val == target

    def add(self, num: int) -> None:
        update = [self.head] * self.MAX_LEVEL
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].val < num:
                curr = curr.forward[i]
            update[i] = curr
        lvl = self._random_level()
        if lvl > self.level:
            self.level = lvl
        node = _SkipNode(num, lvl)
        for i in range(lvl):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def erase(self, num: int) -> bool:
        update = [self.head] * self.MAX_LEVEL
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].val < num:
                curr = curr.forward[i]
            update[i] = curr
        target = curr.forward[0]
        if target is None or target.val != num:
            return False
        for i in range(len(target.forward)):
            if update[i].forward[i] is target:
                update[i].forward[i] = target.forward[i]
        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1
        return True
