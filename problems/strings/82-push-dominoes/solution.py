class Solution:
    def pushDominoes(self, dominoes: str) -> str:
        arr = list(dominoes)
        n = len(arr)
        prev_i = -1
        prev_c = 'L'
        for i in range(n + 1):
            cur_c = arr[i] if i < n else 'R'
            if cur_c == '.':
                continue
            if prev_c == cur_c:
                for k in range(prev_i + 1, i):
                    arr[k] = cur_c
            elif prev_c == 'R' and cur_c == 'L':
                l, r = prev_i + 1, i - 1
                while l < r:
                    arr[l] = 'R'
                    arr[r] = 'L'
                    l += 1
                    r -= 1
            prev_i, prev_c = i, cur_c
        return "".join(arr)
