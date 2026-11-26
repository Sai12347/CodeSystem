class Solution:
    def compareVersion(self, version1: str, version2: str) -> int:
        a, b = version1.split('.'), version2.split('.')
        for i in range(max(len(a), len(b))):
            x = a[i].lstrip('0') if i < len(a) else ''
            y = b[i].lstrip('0') if i < len(b) else ''
            if len(x) != len(y):
                return 1 if len(x) > len(y) else -1
            if x != y:
                return 1 if x > y else -1
        return 0
