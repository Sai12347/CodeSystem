class Solution {
    public int countSubstrings(String s) {
        int m = s.length();
        char[] t = new char[2 * m + 3];
        t[0] = '^';
        t[1] = '#';
        for (int i = 0; i < m; i++) {
            t[2 * i + 2] = s.charAt(i);
            t[2 * i + 3] = '#';
        }
        t[2 * m + 2] = '$';

        int n = t.length;
        int[] p = new int[n];
        int center = 0;
        int right = 0;
        int total = 0;
        for (int i = 1; i < n - 1; i++) {
            if (i < right) {
                int mirror = 2 * center - i;
                p[i] = Math.min(right - i, p[mirror]);
            }
            while (t[i + 1 + p[i]] == t[i - 1 - p[i]]) {
                p[i]++;
            }
            if (i + p[i] > right) {
                center = i;
                right = i + p[i];
            }
            total += (p[i] + 1) / 2;
        }
        return total;
    }
}
