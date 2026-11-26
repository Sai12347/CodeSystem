class Solution:
    def convert(self, s: str, numRows: int) -> str:
        n = len(s)
        if numRows == 1 or numRows >= n:
            return s
        cycle = 2 * (numRows - 1)
        out = []
        for r in range(numRows):
            for i in range(r, n, cycle):
                out.append(s[i])
                if 0 < r < numRows - 1:
                    diag = i + cycle - 2 * r
                    if diag < n:
                        out.append(s[diag])
        return "".join(out)
