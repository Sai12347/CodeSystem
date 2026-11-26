class Solution:
    def rotateTheBox(self, box: List[List[str]]) -> List[List[str]]:
        m, n = len(box), len(box[0])
        res = [['.'] * m for _ in range(n)]
        for r in range(m):
            dest_col = m - 1 - r
            write = n - 1
            for c in range(n - 1, -1, -1):
                ch = box[r][c]
                if ch == '*':
                    res[c][dest_col] = '*'
                    write = c - 1
                elif ch == '#':
                    res[write][dest_col] = '#'
                    write -= 1
        return res
