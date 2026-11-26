class Solution:
    def findMaximumXOR(self, nums: List[int]) -> int:
        max_val = max(nums)
        if max_val == 0:
            return 0
        high_bit = max_val.bit_length() - 1
        root = [None, None]
        best = 0

        for num in nums:
            node = root
            xor_node = root
            cur_xor = 0
            for bit_pos in range(high_bit, -1, -1):
                bit = (num >> bit_pos) & 1
                if node[bit] is None:
                    node[bit] = [None, None]
                node = node[bit]

                toggled = bit ^ 1
                if xor_node[toggled] is not None:
                    cur_xor |= (1 << bit_pos)
                    xor_node = xor_node[toggled]
                else:
                    xor_node = xor_node[bit]
            if cur_xor > best:
                best = cur_xor

        return best
