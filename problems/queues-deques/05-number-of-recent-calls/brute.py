class RecentCounter:
    def __init__(self):
        self.times = []

    def ping(self, t: int) -> int:
        self.times.append(t)
        cutoff = t - 3000
        return sum(1 for x in self.times if x >= cutoff)
