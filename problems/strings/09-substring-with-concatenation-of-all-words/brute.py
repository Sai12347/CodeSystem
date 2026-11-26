class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []
        word_len = len(words[0])
        num_words = len(words)
        total_len = word_len * num_words
        need = Counter(words)
        res = []
        for i in range(len(s) - total_len + 1):
            seen = {}
            ok = True
            for j in range(num_words):
                start = i + j * word_len
                w = s[start:start + word_len]
                limit = need.get(w, 0)
                if limit == 0:
                    ok = False
                    break
                cnt = seen.get(w, 0) + 1
                if cnt > limit:
                    ok = False
                    break
                seen[w] = cnt
            if ok:
                res.append(i)
        return res
