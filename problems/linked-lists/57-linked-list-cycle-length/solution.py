class Solution:
    def cycleLength(self, next: List[int], start: int) -> int:
        slow = start
        fast = start
        while fast != -1 and next[fast] != -1:
            slow = next[slow]
            fast = next[next[fast]]
            if slow == fast:
                length = 1
                curr = next[slow]
                while curr != slow:
                    curr = next[curr]
                    length += 1
                return length
        return 0
