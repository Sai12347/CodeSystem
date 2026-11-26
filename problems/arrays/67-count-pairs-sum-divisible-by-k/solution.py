class Solution:
    def countPairsDivisibleByK(self, nums: List[int], k: int) -> int:
        counts = [0] * k
        answer = 0
        for x in nums:
            r = x % k
            answer += counts[(-r) % k]
            counts[r] += 1
        return answer
