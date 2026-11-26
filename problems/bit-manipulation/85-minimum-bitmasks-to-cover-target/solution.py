class Solution:
    def minMasksToCover(self, target: int, masks: List[int]) -> int:
        if target == 0:
            return 0
        all_or = 0
        for x in masks:
            all_or |= x
        if (all_or & target) != target:
            return -1
        pos = [b for b in range(16) if (target >> b) & 1]
        b_cnt = len(pos)
        projs = set()
        for x in masks:
            p = 0
            for idx, bit in enumerate(pos):
                if (x >> bit) & 1:
                    p |= 1 << idx
            if p:
                projs.add(p)
        # Drop any projected mask dominated by another
        plist = sorted(projs, key=lambda v: v.bit_count(), reverse=True)
        filtered = []
        for p in plist:
            if not any((p & q) == p for q in filtered):
                filtered.append(p)
        full = (1 << b_cnt) - 1
        INF = 100
        dp = [INF] * (full + 1)
        dp[0] = 0
        for p in filtered:
            for s in range(full, -1, -1):
                cur = dp[s]
                if cur + 1 < dp[s | p]:
                    dp[s | p] = cur + 1
        return -1 if dp[full] >= INF else dp[full]
