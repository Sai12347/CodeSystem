class Solution:
    def deleteAllDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0, head)
        prev = dummy
        curr = head
        while curr is not None:
            if curr.next is not None and curr.val == curr.next.val:
                dup = curr.val
                while curr is not None and curr.val == dup:
                    curr = curr.next
                prev.next = curr
            else:
                prev = curr
                curr = curr.next
        return dummy.next
