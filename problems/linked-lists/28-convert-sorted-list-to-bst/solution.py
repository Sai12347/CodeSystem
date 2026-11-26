class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next
        cursor = [head]

        def build(lo: int, hi: int) -> Optional[TreeNode]:
            if lo > hi:
                return None
            mid = (lo + hi + 1) // 2
            left = build(lo, mid - 1)
            node = TreeNode(cursor[0].val)
            cursor[0] = cursor[0].next
            node.left = left
            node.right = build(mid + 1, hi)
            return node

        return build(0, n - 1)
