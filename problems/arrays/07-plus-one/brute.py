class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        val = 0
        for d in digits:
            val = val * 10 + d
        val += 1
        return [int(ch) for ch in str(val)]
