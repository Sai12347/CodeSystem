import heapq


class Solution:
    def kthSmallestInLists(self, lists: List[Optional[ListNode]], k: int) -> int:
        heap: list[tuple[int, int, ListNode]] = []
        for idx, head in enumerate(lists):
            if head is not None:
                heapq.heappush(heap, (head.val, idx, head))
        ans = 0
        for _ in range(k):
            val, idx, node = heapq.heappop(heap)
            ans = val
            if node.next is not None:
                heapq.heappush(heap, (node.next.val, idx, node.next))
        return ans
