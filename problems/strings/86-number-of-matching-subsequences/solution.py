class Solution:
    def numMatchingSubseq(self, s: str, words: List[str]) -> int:
        buckets = [[] for _ in range(26)]
        for w in words:
            buckets[ord(w[0]) - 97].append((w, 0))
        ans = 0
        for ch in s:
            idx = ord(ch) - 97
            cur = buckets[idx]
            buckets[idx] = []
            for w, pos in cur:
                nxt = pos + 1
                if nxt == len(w):
                    ans += 1
                else:
                    buckets[ord(w[nxt]) - 97].append((w, nxt))
        return ans
