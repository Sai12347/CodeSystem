class Solution {
    public int minMasksToCover(int target, int[] masks) {
        if (target == 0) return 0;
        int allOr = 0;
        for (int x : masks) allOr |= x;
        if ((allOr & target) != target) return -1;

        int[] pos = new int[16];
        int bCnt = 0;
        for (int b = 0; b < 16; b++) {
            if (((target >> b) & 1) != 0) pos[bCnt++] = b;
        }
        Set<Integer> projSet = new HashSet<>();
        for (int x : masks) {
            int p = 0;
            for (int i = 0; i < bCnt; i++) {
                if (((x >> pos[i]) & 1) != 0) p |= (1 << i);
            }
            if (p != 0) projSet.add(p);
        }
        List<Integer> plist = new ArrayList<>(projSet);
        plist.sort((a, b) -> Integer.compare(Integer.bitCount(b), Integer.bitCount(a)));
        List<Integer> filtered = new ArrayList<>();
        for (int p : plist) {
            boolean dominated = false;
            for (int q : filtered) {
                if ((p & q) == p) {
                    dominated = true;
                    break;
                }
            }
            if (!dominated) filtered.add(p);
        }
        int full = (1 << bCnt) - 1;
        int INF = 100;
        int[] dp = new int[full + 1];
        Arrays.fill(dp, INF);
        dp[0] = 0;
        for (int p : filtered) {
            for (int s = full; s >= 0; s--) {
                int cur = dp[s];
                if (cur + 1 < dp[s | p]) {
                    dp[s | p] = cur + 1;
                }
            }
        }
        return dp[full] >= INF ? -1 : dp[full];
    }
}
