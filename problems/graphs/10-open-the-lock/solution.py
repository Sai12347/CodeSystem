class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        dead = set(deadends)
        if "0000" in dead:
            return -1
        if target == "0000":
            return 0

        begin = {"0000"}
        end = {target}
        visited = {"0000", target}
        steps = 0

        while begin and end:
            if len(begin) > len(end):
                begin, end = end, begin
            steps += 1
            next_front = set()
            for code in begin:
                for i in range(4):
                    d = int(code[i])
                    prefix = code[:i]
                    suffix = code[i + 1 :]
                    for nd in ((d + 1) % 10, (d + 9) % 10):
                        nxt = prefix + str(nd) + suffix
                        if nxt in dead:
                            continue
                        if nxt in end:
                            return steps
                        if nxt not in visited:
                            visited.add(nxt)
                            next_front.add(nxt)
            begin = next_front

        return -1
