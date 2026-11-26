class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        vals = []
        for head in (list1, list2):
            curr = head
            while curr is not None:
                vals.append(curr.val)
                curr = curr.next
        vals.sort()
        dummy = ListNode(0)
        tail = dummy
        for v in vals:
            tail.next = ListNode(v)
            tail = tail.next
        return dummy.next
