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

    public int countComponents(int n, int[][] edges) {
        parent = new int[n];
        rank = new int[n];
        for (int i = 0; i < n; i++) parent[i] = i;

        int components = n;
        for (int[] e : edges) {
            int ru = find(e[0]), rv = find(e[1]);
            if (ru != rv) {
                if (rank[ru] < rank[rv]) {
                    int tmp = ru;
                    ru = rv;
                    rv = tmp;
                }
                parent[rv] = ru;
                if (rank[ru] == rank[rv]) rank[ru]++;
                components--;
            }
        }
        return components;
    }
}
