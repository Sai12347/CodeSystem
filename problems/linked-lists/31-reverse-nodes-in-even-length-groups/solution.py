class Solution:
    def reverseEvenLengthGroups(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = head
        group_len = 2
        while prev.next is not None:
            node = prev
            count = 0
            while count < group_len and node.next is not None:
                node = node.next
                count += 1
            if count % 2 == 0:
                group_head = prev.next
                nxt_group = node.next
                rprev = nxt_group
                curr = group_head
                for _ in range(count):
                    nxt = curr.next
                    curr.next = rprev
                    rprev = curr
                    curr = nxt
                prev.next = rprev
                prev = group_head
            else:
                prev = node
            group_len += 1
        return head
