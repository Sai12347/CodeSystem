class Solution:
    def numOfSubarrays(self, nums: List[int]) -> int:
        even, odd, parity, answer = 1, 0, 0, 0
        for x in nums:
            parity ^= x & 1
            answer += even if parity else odd
            if parity: odd += 1
            else: even += 1
        return answer
