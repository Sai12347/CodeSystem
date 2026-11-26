class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        heap = []
        cur_max = -10**9
        for i, row in enumerate(nums):
            val = row[0]
            heap.append((val, i, 0))
            if val > cur_max:
                cur_max = val
        heapq.heapify(heap)
        best_l, best_r = heap[0][0], cur_max
        while True:
            cur_min, r, c = heapq.heappop(heap)
            if cur_max - cur_min < best_r - best_l or (
                cur_max - cur_min == best_r - best_l and cur_min < best_l
            ):
                best_l, best_r = cur_min, cur_max
            if c + 1 == len(nums[r]):
                break
            nxt = nums[r][c + 1]
            if nxt > cur_max:
                cur_max = nxt
            heapq.heappush(heap, (nxt, r, c + 1))
        return [best_l, best_r]
