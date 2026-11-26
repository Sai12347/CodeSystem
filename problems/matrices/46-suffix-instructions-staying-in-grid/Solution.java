class Solution {
    public int[] executeInstructions(int n, int[] startPos, String s) {
        int m = s.length();
        int sr = startPos[0], sc = startPos[1];
        int[] pr = new int[m + 1];
        int[] pc = new int[m + 1];
        for (int i = 0; i < m; i++) {
            char ch = s.charAt(i);
            int dr = ch == 'U' ? -1 : (ch == 'D' ? 1 : 0);
            int dc = ch == 'L' ? -1 : (ch == 'R' ? 1 : 0);
            pr[i + 1] = pr[i] + dr;
            pc[i + 1] = pc[i] + dc;
        }
        int[] ans = new int[m];
        Map<Integer, Integer> rowSeen = new HashMap<>();
        Map<Integer, Integer> colSeen = new HashMap<>();
        for (int i = m - 1; i >= 0; i--) {
            rowSeen.put(pr[i + 1], i + 1);
            colSeen.put(pc[i + 1], i + 1);
            int stop = m + 1;
            Integer t1 = rowSeen.get(pr[i] - sr - 1);
            if (t1 != null && t1 < stop) stop = t1;
            Integer t2 = rowSeen.get(pr[i] + n - sr);
            if (t2 != null && t2 < stop) stop = t2;
            Integer t3 = colSeen.get(pc[i] - sc - 1);
            if (t3 != null && t3 < stop) stop = t3;
            Integer t4 = colSeen.get(pc[i] + n - sc);
            if (t4 != null && t4 < stop) stop = t4;
            ans[i] = stop - 1 - i;
        }
        return ans;
    }
}
