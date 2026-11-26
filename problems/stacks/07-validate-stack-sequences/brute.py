class Solution:
    def validateStackSequences(self, pushed: List[int], popped: List[int]) -> bool:
        # Independent mathematical characterization:
        # Map values to their push index (rank). For every popped[i], all elements
        # popped AFTER i whose rank is smaller than rank(popped[i]) were already
        # below popped[i] on the stack, so they must be popped in strictly
        # decreasing order of rank (no 3-1-2 pattern).
        rank = {val: idx for idx, val in enumerate(pushed)}
        seq = [rank[val] for val in popped]
        n = len(seq)
        for i in range(n):
            cur = seq[i]
            prev_smaller = cur
            for j in range(i + 1, n):
                if seq[j] < cur:
                    if seq[j] > prev_smaller:
                        return False
                    prev_smaller = seq[j]
        return True
