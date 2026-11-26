class Solution:
    def minAlignedBlocks(self, start: int, n: int) -> int:
        blocks = 0
        cur = start
        rem = n
        while rem > 0:
            max_step = 1 << (rem.bit_length() - 1)
            if cur == 0:
                step = max_step
            else:
                low = cur & -cur
                step = low if low < max_step else max_step
            cur += step
            rem -= step
            blocks += 1
        return blocks
