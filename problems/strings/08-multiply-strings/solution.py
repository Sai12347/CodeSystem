class Solution:
    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"
        m, n = len(num1), len(num2)
        res = [0] * (m + n)
        for i in range(m - 1, -1, -1):
            d1 = ord(num1[i]) - 48
            for j in range(n - 1, -1, -1):
                d2 = ord(num2[j]) - 48
                total = d1 * d2 + res[i + j + 1]
                res[i + j + 1] = total % 10
                res[i + j] += total // 10
        idx = 0
        while idx < len(res) and res[idx] == 0:
            idx += 1
        return "".join(chr(d + 48) for d in res[idx:])
