class Solution:
    def kthSmallestSubsetXor(self, nums: List[int], k: int) -> int:
        basis = [0] * 30
        for x in nums:
            v = x
            for b in range(29, -1, -1):
                if (v >> b) & 1:
                    if basis[b] == 0:
                        basis[b] = v
                        break
                    v ^= basis[b]
        for b in range(30):
            if basis[b]:
                for high in range(b + 1, 30):
                    if (basis[high] >> b) & 1:
                        basis[high] ^= basis[b]
        vecs = [basis[b] for b in range(30) if basis[b]]
        r = len(vecs)
        if k > (1 << r):
            return -1
        idx = k - 1
        ans = 0
        for i in range(r):
            if (idx >> i) & 1:
                ans ^= vecs[i]
        return ans
