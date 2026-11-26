class Solution {
    public int shortestWay(String source, String target) {
        int m = source.length();
        int[][] nxt = new int[m + 1][26];
        Arrays.fill(nxt[m], -1);
        for (int i = m - 1; i >= 0; i--) {
            System.arraycopy(nxt[i + 1], 0, nxt[i], 0, 26);
            nxt[i][source.charAt(i) - 'a'] = i;
        }
        int ans = 1, pos = 0;
        for (int i = 0; i < target.length(); i++) {
            int c = target.charAt(i) - 'a';
            if (nxt[0][c] == -1) return -1;
            if (nxt[pos][c] == -1) {
                ans++;
                pos = 0;
            }
            pos = nxt[pos][c] + 1;
        }
        return ans;
    }
}
