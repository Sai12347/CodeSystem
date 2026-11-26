class Solution:
    def deleteNodes(self, head: Optional[ListNode], m: int, n: int) -> Optional[ListNode]:
        curr = head
        while curr is not None:
            for _ in range(m - 1):
                if curr.next is None:
                    return head
                curr = curr.next
            skip = curr.next
            for _ in range(n):
                if skip is None:
                    break
                skip = skip.next
            curr.next = skip
            curr = skip
        return head
