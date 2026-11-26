import heapq


class Solution:
    def sortKSortedList(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None or head.next is None or k == 0:
            return head
        heap: list[tuple[int, int, ListNode]] = []
        curr = head
        uid = 0
        for _ in range(k + 1):
            if curr is None:
                break
            heapq.heappush(heap, (curr.val, uid, curr))
            uid += 1
            curr = curr.next
        dummy = ListNode(0)
        tail = dummy
        while heap:
            _, _, node = heapq.heappop(heap)
            tail.next = node
            tail = node
            if curr is not None:
                heapq.heappush(heap, (curr.val, uid, curr))
                uid += 1
                curr = curr.next
        tail.next = None
        return dummy.next
