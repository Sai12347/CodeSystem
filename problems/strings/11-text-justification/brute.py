class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res = []
        cur = []
        num_letters = 0
        for w in words:
            if num_letters + len(w) + len(cur) > maxWidth:
                gaps = max(1, len(cur) - 1)
                for s in range(maxWidth - num_letters):
                    cur[s % gaps] += " "
                res.append("".join(cur))
                cur = []
                num_letters = 0
            cur.append(w)
            num_letters += len(w)
        res.append(" ".join(cur).ljust(maxWidth))
        return res
