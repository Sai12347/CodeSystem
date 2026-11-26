class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        # Independent strategy: match each heaviest person with the heaviest compatible partner
        arr = sorted(people)
        used = [False] * len(arr)
        boats = 0
        for i in range(len(arr) - 1, -1, -1):
            if used[i]:
                continue
            used[i] = True
            need = limit - arr[i]
            # Find heaviest unused partner j < i with arr[j] <= need
            j = bisect.bisect_right(arr, need, 0, i) - 1
            while j >= 0 and used[j]:
                j -= 1
            if j >= 0:
                used[j] = True
            boats += 1
        return boats
