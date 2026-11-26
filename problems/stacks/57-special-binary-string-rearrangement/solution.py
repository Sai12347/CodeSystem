class Solution:
    def makeLargestSpecial(self, s: str) -> str:
        frames = [[]]
        for ch in s:
            if ch == '1':
                frames.append([])
            else:
                inner = frames.pop()
                inner.sort(reverse=True)
                frames[-1].append("1" + "".join(inner) + "0")
        frames[0].sort(reverse=True)
        return "".join(frames[0])
