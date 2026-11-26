class MyCalendarThree:
    def __init__(self):
        self.delta=defaultdict(int)

    def book(self, start: int, end: int) -> int:
        self.delta[start]+=1;self.delta[end]-=1
        active=best=0
        for x in sorted(self.delta):
            active+=self.delta[x];best=max(best,active)
        return best
