class Solution:
    def canSortBySetBits(self, nums: List[int]) -> bool:
        prev_max = 0
        cur_pop = nums[0].bit_count()
        cur_min = nums[0]
        cur_max = nums[0]
        for x in nums[1:]:
            p = x.bit_count()
            if p == cur_pop:
                if x < cur_min:
                    cur_min = x
                if x > cur_max:
                    cur_max = x
            else:
                if cur_min < prev_max:
                    return False
                prev_max = cur_max
                cur_pop = p
                cur_min = x
                cur_max = x
        return cur_min >= prev_max
