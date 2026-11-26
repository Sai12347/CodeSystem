class Solution:
    def countVowelSubstrings(self, word: str) -> int:
        vidx = {'a': 0, 'e': 1, 'i': 2, 'o': 3, 'u': 4}
        last_v = [-1] * 5
        last_c = -1
        ans = 0
        for i, ch in enumerate(word):
            if ch in vidx:
                last_v[vidx[ch]] = i
                m = min(last_v)
                if m > last_c:
                    ans += m - last_c
            else:
                last_c = i
        return ans
