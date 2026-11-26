class Solution:
    def numberOfGoodPairs(self, nums: List[int]) -> int:
        counts = Counter()
        answer = 0
        for x in nums:
            answer += counts[x]
            counts[x] += 1
        return answer
