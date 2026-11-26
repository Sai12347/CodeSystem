class Solution:
    def modifiedList(self, nums: List[int], head: Optional[ListNode]) -> Optional[ListNode]:
        ban = set(nums)
        dummy = ListNode(0, head)
        curr = dummy
        while curr.next is not None:
            if curr.next.val in ban:
                curr.next = curr.next.next
            else:
                curr = curr.next
        return dummy.next
