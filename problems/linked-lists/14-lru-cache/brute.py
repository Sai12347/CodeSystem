class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.items = []  # ordered LRU -> MRU

    def get(self, key: int) -> int:
        for i, pair in enumerate(self.items):
            if pair[0] == key:
                self.items.append(self.items.pop(i))
                return pair[1]
        return -1

    def put(self, key: int, value: int) -> None:
        for i, pair in enumerate(self.items):
            if pair[0] == key:
                pair[1] = value
                self.items.append(self.items.pop(i))
                return
        if len(self.items) == self.capacity:
            self.items.pop(0)
        self.items.append([key, value])
