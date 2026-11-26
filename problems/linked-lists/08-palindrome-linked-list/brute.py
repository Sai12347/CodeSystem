class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        vals = []
        curr = head
        while curr is not None:
            vals.append(curr.val)
            curr = curr.next
        return vals == vals[::-1]
