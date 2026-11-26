class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        for loc in range(1001):
            cur = 0
            for passengers, start, end in trips:
                if start <= loc < end:
                    cur += passengers
            if cur > capacity:
                return False
        return True
