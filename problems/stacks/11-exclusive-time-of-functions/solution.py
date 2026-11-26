class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        res = [0] * n
        stack = []
        prev = 0
        for entry in logs:
            fid_str, kind, ts_str = entry.split(":")
            fid = int(fid_str)
            ts = int(ts_str)
            if kind == "start":
                if stack:
                    res[stack[-1]] += ts - prev
                stack.append(fid)
                prev = ts
            else:
                res[stack.pop()] += ts - prev + 1
                prev = ts + 1
        return res
