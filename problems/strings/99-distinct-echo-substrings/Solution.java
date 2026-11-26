class Solution {
    public int distinctEchoSubstrings(String text) {
        int n = text.length();
        long m1 = 1000000007L, m2 = 1000000009L;
        long b1 = 31L, b2 = 37L;
        long[] h1 = new long[n + 1], h2 = new long[n + 1];
        long[] p1 = new long[n + 1], p2 = new long[n + 1];
        p1[0] = p2[0] = 1;
        for (int i = 0; i < n; i++) {
            int v = text.charAt(i) - 'a' + 1;
            h1[i + 1] = (h1[i] * b1 + v) % m1;
            h2[i + 1] = (h2[i] * b2 + v) % m2;
            p1[i + 1] = (p1[i] * b1) % m1;
            p2[i + 1] = (p2[i] * b2) % m2;
        }
        int total = 0;
        for (int half = 1; half <= n / 2; half++) {
            long pw1 = p1[half], pw2 = p2[half];
            HashSet<Long> seen = new HashSet<>();
            for (int i = 0; i + 2 * half <= n; i++) {
                long a1 = (h1[i + half] - h1[i] * pw1 % m1 + m1) % m1;
                long b1v = (h1[i + 2 * half] - h1[i + half] * pw1 % m1 + m1) % m1;
                if (a1 == b1v) {
                    long a2 = (h2[i + half] - h2[i] * pw2 % m2 + m2) % m2;
                    long b2v = (h2[i + 2 * half] - h2[i + half] * pw2 % m2 + m2) % m2;
                    if (a2 == b2v) {
                        seen.add((a1 << 32) ^ a2);
                    }
                }
            }
            total += seen.size();
        }
        return total;
    }
}
