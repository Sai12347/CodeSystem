class Solution:
    def peakStackMemory(self, events: List[str]) -> int:
        stack = []
        cur = 0
        peak = 0
        for ev in events:
            if ev == "RET":
                cur -= stack.pop()
            elif ev[0] == "C":
                val = int(ev[5:])
                stack.append(val)
                cur += val
                if cur > peak:
                    peak = cur
            elif ev[0] == "A":
                val = int(ev[6:])
                stack[-1] += val
                cur += val
                if cur > peak:
                    peak = cur
            else:
                val = int(ev[7:])
                freed = stack[-1] if stack[-1] < val else val
                stack[-1] -= freed
                cur -= freed
        return peak
