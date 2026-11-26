class Solution {
    public int longestDupSubstringLength(String s) {
        int n = s.length();
        if (n <= 1) return 0;
        long m1 = 1000000007L, m2 = 1000000009L;
        long b1 = 31L, b2 = 37L;
        long[] h1 = new long[n + 1], h2 = new long[n + 1];
        long[] p1 = new long[n + 1], p2 = new long[n + 1];
        p1[0] = p2[0] = 1;
        for (int i = 0; i < n; i++) {
            int v = s.charAt(i) - 'a' + 1;
            h1[i + 1] = (h1[i] * b1 + v) % m1;
            h2[i + 1] = (h2[i] * b2 + v) % m2;
            p1[i + 1] = (p1[i] * b1) % m1;
            p2[i + 1] = (p2[i] * b2) % m2;
        }
        int lo = 0, hi = n - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >>> 1;
            if (hasDup(mid, n, h1, h2, p1[mid], p2[mid], m1, m2)) lo = mid;
            else hi = mid - 1;
        }
        return lo;
    }
    private boolean hasDup(int len, int n, long[] h1, long[] h2, long pw1, long pw2, long m1, long m2) {
        HashSet<Long> seen = new HashSet<>(n - len + 1);
        for (int i = 0; i + len <= n; i++) {
            long x1 = (h1[i + len] - h1[i] * pw1 % m1 + m1) % m1;
            long x2 = (h2[i + len] - h2[i] * pw2 % m2 + m2) % m2;
            long key = (x1 << 32) ^ x2;
            if (!seen.add(key)) return true;
        }
        return false;
    }
}
