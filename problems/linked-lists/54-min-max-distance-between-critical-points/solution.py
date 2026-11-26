class Solution:
    def nodesBetweenCriticalPoints(self, head: Optional[ListNode]) -> List[int]:
        first_idx = -1
        prev_idx = -1
        min_dist = 10**9
        prev = head
        curr = head.next
        idx = 1
        while curr is not None and curr.next is not None:
            nxt = curr.next
            if (curr.val > prev.val and curr.val > nxt.val) or (curr.val < prev.val and curr.val < nxt.val):
                if first_idx == -1:
                    first_idx = idx
                else:
                    diff = idx - prev_idx
                    if diff < min_dist:
                        min_dist = diff
                prev_idx = idx
            prev = curr
            curr = nxt
            idx += 1
        if min_dist == 10**9:
            return [-1, -1]
        return [min_dist, prev_idx - first_idx]
