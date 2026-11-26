class Solution:
    def countInversions(self, head: Optional[ListNode]) -> int:
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next

        def sort_count(node: Optional[ListNode], length: int) -> tuple[Optional[ListNode], int]:
            if length <= 1 or node is None:
                return node, 0
            left_len = length // 2
            right_len = length - left_len
            mid = node
            for _ in range(left_len - 1):
                mid = mid.next
            right_head = mid.next
            mid.next = None

            left, inv_l = sort_count(node, left_len)
            right, inv_r = sort_count(right_head, right_len)
            inv = inv_l + inv_r
            left_rem = left_len

            dummy = ListNode(0)
            tail = dummy
            while left is not None and right is not None:
                if left.val <= right.val:
                    tail.next = left
                    left = left.next
                    left_rem -= 1
                else:
                    tail.next = right
                    right = right.next
                    inv += left_rem
                tail = tail.next
            tail.next = left if left is not None else right
            return dummy.next, inv

        _, ans = sort_count(head, n)
        return ans
