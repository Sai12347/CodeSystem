class LFUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.store = {}  # key -> [val, freq, tick]
        self.tick = 0

    def get(self, key: int) -> int:
        if key not in self.store:
            return -1
        self.tick += 1
        entry = self.store[key]
        entry[1] += 1
        entry[2] = self.tick
        return entry[0]

    def put(self, key: int, value: int) -> None:
        if self.capacity <= 0:
            return
        self.tick += 1
        if key in self.store:
            entry = self.store[key]
            entry[0] = value
            entry[1] += 1
            entry[2] = self.tick
            return
        if len(self.store) == self.capacity:
            victim = min(self.store, key=lambda k: (self.store[k][1], self.store[k][2]))
            del self.store[victim]
        self.store[key] = [value, 1, self.tick]
