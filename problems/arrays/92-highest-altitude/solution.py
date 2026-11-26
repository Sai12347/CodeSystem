class Solution:
    def largestAltitude(self, gain: List[int]) -> int:
        altitude = best = 0
        for x in gain: altitude += x; best = max(best, altitude)
        return best
