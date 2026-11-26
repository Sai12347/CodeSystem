class Solution {
    private int[] parent;
    private int[] rank;

    private int find(int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    private boolean isSimilar(String a, String b) {
        int diff = 0;
        int len = a.length();
        for (int i = 0; i < len; i++) {
            if (a.charAt(i) != b.charAt(i)) {
                diff++;
                if (diff > 2) return false;
            }
        }
        return true;
    }

    public int numSimilarGroups(String[] strs) {
        int n = strs.length;
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        int groups = n;
        for (int i = 0; i < n; i++) {
            for (int j = i + 1; j < n; j++) {
                int ri = find(i), rj = find(j);
                if (ri != rj && isSimilar(strs[i], strs[j])) {
                    if (rank[ri] < rank[rj]) {
                        int tmp = ri;
                        ri = rj;
                        rj = tmp;
                    }
                    parent[rj] = ri;
                    if (rank[ri] == rank[rj]) rank[ri]++;
                    groups--;
                }
            }
        }
        return groups;
    }
}
