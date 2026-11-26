class Solution {
    private int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    public int minCostToSupplyWater(int n, int[] wells, int[][] pipes) {
        int m = pipes.length;
        int[][] edges = new int[n + m][3];
        for (int i = 0; i < n; i++) {
            edges[i][0] = 0;
            edges[i][1] = i + 1;
            edges[i][2] = wells[i];
        }
        for (int i = 0; i < m; i++) {
            edges[n + i][0] = pipes[i][0];
            edges[n + i][1] = pipes[i][1];
            edges[n + i][2] = pipes[i][2];
        }
        Arrays.sort(edges, (a, b) -> Integer.compare(a[2], b[2]));

        int[] parent = new int[n + 1];
        int[] size = new int[n + 1];
        for (int i = 0; i <= n; i++) {
            parent[i] = i;
            size[i] = 1;
        }

        int total = 0;
        int components = n + 1;
        for (int[] e : edges) {
            int ru = find(parent, e[0]);
            int rv = find(parent, e[1]);
            if (ru != rv) {
                if (size[ru] < size[rv]) {
                    int tmp = ru;
                    ru = rv;
                    rv = tmp;
                }
                parent[rv] = ru;
                size[ru] += size[rv];
                total += e[2];
                components--;
                if (components == 1) {
                    break;
                }
            }
        }
        return total;
    }
}
