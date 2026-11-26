class Solution:
    def swapNodes(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        lead = head
        for _ in range(k - 1):
            lead = lead.next
        first = lead
        second = head
        while lead.next is not None:
            lead = lead.next
            second = second.next
        first.val, second.val = second.val, first.val
        return head
