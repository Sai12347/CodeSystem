class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res = []
        i = 0
        n = len(words)
        while i < n:
            line_len = len(words[i])
            j = i + 1
            while j < n and line_len + 1 + len(words[j]) <= maxWidth:
                line_len += 1 + len(words[j])
                j += 1
            num_words = j - i
            if j == n or num_words == 1:
                line = " ".join(words[i:j])
                res.append(line + " " * (maxWidth - len(line)))
            else:
                words_chars = sum(len(words[k]) for k in range(i, j))
                total_spaces = maxWidth - words_chars
                gaps = num_words - 1
                base, extra = divmod(total_spaces, gaps)
                parts = []
                for k in range(i, j - 1):
                    parts.append(words[k])
                    parts.append(" " * (base + (1 if k - i < extra else 0)))
                parts.append(words[j - 1])
                res.append("".join(parts))
            i = j
        return res
