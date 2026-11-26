class Solution {
    private int[] parent;
    private int[] rank;
    private int components;

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
        components--;
    }

    public int regionsBySlashes(String[] grid) {
        int n = grid.length;
        int total = 4 * n * n;
        parent = new int[total];
        rank = new int[total];
        for (int i = 0; i < total; i++) parent[i] = i;
        components = total;

        for (int r = 0; r < n; r++) {
            String row = grid[r];
            for (int c = 0; c < n; c++) {
                int base = 4 * (r * n + c);
                char ch = row.charAt(c);
                if (ch == '/') {
                    union(base + 0, base + 3);
                    union(base + 1, base + 2);
                } else if (ch == '\\') {
                    union(base + 0, base + 1);
                    union(base + 2, base + 3);
                } else {
                    union(base + 0, base + 1);
                    union(base + 1, base + 2);
                    union(base + 2, base + 3);
                }

                if (r + 1 < n) {
                    union(base + 2, 4 * ((r + 1) * n + c) + 0);
                }
                if (c + 1 < n) {
                    union(base + 1, 4 * (r * n + (c + 1)) + 3);
                }
            }
        }
        return components;
    }
}
