class Solution:
    def kthSmallestRowSum(self, mat: List[List[int]], k: int) -> int:
        cur = mat[0][:k]
        for row in mat[1:]:
            heap = [(cur[i] + row[0], i, 0) for i in range(len(cur))]
            heapq.heapify(heap)
            nxt = []
            while heap and len(nxt) < k:
                s, i, j = heapq.heappop(heap)
                nxt.append(s)
                if j + 1 < len(row):
                    heapq.heappush(heap, (cur[i] + row[j + 1], i, j + 1))
            cur = nxt
        return cur[k - 1]
