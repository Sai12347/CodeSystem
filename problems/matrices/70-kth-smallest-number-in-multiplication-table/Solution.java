class Solution {
    public int findKthNumber(int m, int n, int k) {
        if (m > n) {
            int tmp = m;
            m = n;
            n = tmp;
        }
        int lo = 1, hi = m * n;
        while (lo < hi) {
            int mid = lo + (hi - lo) / 2;
            int cnt = 0;
            for (int i = 1; i <= m; i++) {
                int q = mid / i;
                if (q == 0) break;
                cnt += Math.min(q, n);
            }
            if (cnt >= k) hi = mid;
            else lo = mid + 1;
        }
        return lo;
    }
}
