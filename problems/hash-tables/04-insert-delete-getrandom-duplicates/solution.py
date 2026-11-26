import random


class RandomizedCollection:
    def __init__(self):
        self.vals = []
        self.pos = defaultdict(set)

    def insert(self, val: int) -> bool:
        was_absent = len(self.pos[val]) == 0
        self.pos[val].add(len(self.vals))
        self.vals.append(val)
        return was_absent

    def remove(self, val: int) -> bool:
        if not self.pos[val]:
            return False
        remove_idx = self.pos[val].pop()
        last_idx = len(self.vals) - 1
        last_val = self.vals[last_idx]
        if remove_idx != last_idx:
            self.vals[remove_idx] = last_val
            self.pos[last_val].remove(last_idx)
            self.pos[last_val].add(remove_idx)
        self.vals.pop()
        if not self.pos[val]:
            del self.pos[val]
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)
