class Solution:
    def sortLinkedList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None:
            return None
        curr = head
        while curr.next is not None:
            if curr.next.val < 0:
                node = curr.next
                curr.next = node.next
                node.next = head
                head = node
            else:
                curr = curr.next
        return head
