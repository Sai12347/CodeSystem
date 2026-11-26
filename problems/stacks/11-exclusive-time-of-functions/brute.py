class Solution:
    def exclusiveTime(self, n: int, logs: List[str]) -> List[int]:
        # Independent interval-accounting approach:
        # Each call frame stores [fid, start_ts, direct_children_inclusive_time].
        # When a call ends, its inclusive duration is (end_ts - start_ts + 1),
        # its exclusive time is (inclusive - direct_children_inclusive_time),
        # and its inclusive duration is added to its parent's children total.
        res = [0] * n
        frames = []
        for entry in logs:
            fid_str, kind, ts_str = entry.split(":")
            fid = int(fid_str)
            ts = int(ts_str)
            if kind == "start":
                frames.append([fid, ts, 0])
            else:
                f_id, start_ts, child_time = frames.pop()
                inclusive = ts - start_ts + 1
                res[f_id] += inclusive - child_time
                if frames:
                    frames[-1][2] += inclusive
        return res
