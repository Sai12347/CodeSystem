class Solution:
    def reverseAlternateAndAppend(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        odd = head
        rev_even = None
        while odd.next is not None:
            even = odd.next
            odd.next = even.next
            even.next = rev_even
            rev_even = even
            if odd.next is not None:
                odd = odd.next
        odd.next = rev_even
        return head
