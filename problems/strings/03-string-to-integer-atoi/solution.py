class Solution:
    def myAtoi(self, s: str) -> int:
        INT_MAX = 2147483647
        INT_MIN = -2147483648
        n = len(s)
        i = 0
        while i < n and s[i] == " ":
            i += 1
        if i == n:
            return 0

        sign = 1
        if s[i] == "-":
            sign = -1
            i += 1
        elif s[i] == "+":
            i += 1

        res = 0
        limit = INT_MAX // 10
        while i < n and "0" <= s[i] <= "9":
            digit = ord(s[i]) - ord("0")
            if res > limit or (res == limit and digit > 7):
                return INT_MAX if sign == 1 else INT_MIN
            res = res * 10 + digit
            i += 1
        return sign * res
