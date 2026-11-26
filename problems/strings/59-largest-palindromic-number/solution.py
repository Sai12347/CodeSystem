class Solution:
    def largestPalindromic(self, num: str) -> str:
        cnt = [0] * 10
        for ch in num:
            cnt[ord(ch) - 48] += 1
        left = []
        for d in range(9, -1, -1):
            if d == 0 and not left:
                break
            pairs = cnt[d] // 2
            if pairs:
                left.append(str(d) * pairs)
                cnt[d] -= pairs * 2
        mid = ""
        for d in range(9, -1, -1):
            if cnt[d] > 0:
                mid = str(d)
                break
        if not left and not mid:
            return "0"
        lstr = "".join(left)
        return lstr + mid + lstr[::-1]
