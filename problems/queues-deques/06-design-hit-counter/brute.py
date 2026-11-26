class HitCounter:
    def __init__(self):
        self.hits = []

    def hit(self, timestamp: int) -> None:
        self.hits.append(timestamp)

    def getHits(self, timestamp: int) -> int:
        cutoff = timestamp - 300
        return sum(1 for x in self.hits if cutoff < x <= timestamp)
