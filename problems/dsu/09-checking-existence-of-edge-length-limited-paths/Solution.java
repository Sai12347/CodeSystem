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

    private void union(int a, int b) {
        int ra = find(a), rb = find(b);
        if (ra == rb) return;
        if (rank[ra] < rank[rb]) {
            int tmp = ra;
            ra = rb;
            rb = tmp;
        }
        parent[rb] = ra;
        if (rank[ra] == rank[rb]) rank[ra]++;
    }

    public boolean[] distanceLimitedPathsExist(int n, int[][] edgeList, int[][] queries) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        Arrays.sort(edgeList, (a, b) -> Integer.compare(a[2], b[2]));

        int qLen = queries.length;
        Integer[] order = new Integer[qLen];
        for (int i = 0; i < qLen; i++) order[i] = i;
        Arrays.sort(order, (i, j) -> Integer.compare(queries[i][2], queries[j][2]));

        boolean[] ans = new boolean[qLen];
        int ei = 0;
        int m = edgeList.length;
        for (int qi : order) {
            int p = queries[qi][0];
            int q = queries[qi][1];
            int limit = queries[qi][2];
            while (ei < m && edgeList[ei][2] < limit) {
                union(edgeList[ei][0], edgeList[ei][1]);
                ei++;
            }
            ans[qi] = find(p) == find(q);
        }
        return ans;
    }
}
