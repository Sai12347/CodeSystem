class Solution:
    def numComponents(self, head: Optional[ListNode], nums: List[int]) -> int:
        present = set(nums)
        ans = 0
        curr = head
        while curr is not None:
            if curr.val in present and (curr.next is None or curr.next.val not in present):
                ans += 1
            curr = curr.next
        return ans
