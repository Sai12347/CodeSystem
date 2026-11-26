class Solution:
    def circularArrayLoop(self, nums: List[int]) -> bool:
        n = len(nums)

        def next_idx(idx: int, forward: bool) -> int:
            if (nums[idx] > 0) != forward:
                return -1
            nxt = (idx + nums[idx]) % n
            if nxt == idx or (nums[nxt] > 0) != forward or nums[nxt] == 0:
                return -1
            return nxt

        for i in range(n):
            if nums[i] == 0:
                continue
            forward = nums[i] > 0
            slow = i
            fast = i
            while True:
                slow = next_idx(slow, forward)
                if slow == -1:
                    break
                fast = next_idx(fast, forward)
                if fast != -1:
                    fast = next_idx(fast, forward)
                if fast == -1:
                    break
                if slow == fast:
                    return True
            curr = i
            while nums[curr] != 0 and (nums[curr] > 0) == forward:
                nxt = (curr + nums[curr]) % n
                nums[curr] = 0
                curr = nxt
        return False
