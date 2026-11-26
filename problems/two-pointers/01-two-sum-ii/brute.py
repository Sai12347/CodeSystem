class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        n = len(numbers)
        for i in range(n):
            need = target - numbers[i]
            for j in range(i + 1, n):
                if numbers[j] == need:
                    return [i + 1, j + 1]
                if numbers[j] > need:
                    break
        return []
