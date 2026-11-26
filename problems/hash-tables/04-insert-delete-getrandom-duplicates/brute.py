import random


class RandomizedCollection:
    def __init__(self):
        self.vals = []

    def insert(self, val: int) -> bool:
        was_absent = val not in self.vals
        self.vals.append(val)
        return was_absent

    def remove(self, val: int) -> bool:
        if val not in self.vals:
            return False
        self.vals.remove(val)
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)
