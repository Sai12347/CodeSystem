class Solution:
    def pancakeSort(self, arr: List[int]) -> List[int]:
        # Independent strategy: place smallest-to-largest by building reverse sorted then final flip
        n = len(arr)
        res = []
        for size in range(n, 1, -1):
            max_idx = max(range(size), key=lambda i: arr[i])
            if max_idx != size - 1:
                arr[:max_idx + 1] = reversed(arr[:max_idx + 1])
                res.append(max_idx + 1)
                arr[:size] = reversed(arr[:size])
                res.append(size)
        return res
