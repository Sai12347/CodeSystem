class Solution {
    private int find(int[] parent, int x) {
        while (parent[x] != x) {
            parent[x] = parent[parent[x]];
            x = parent[x];
        }
        return x;
    }

    public int minimumCost(int n, int[][] connections) {
        if (n <= 1) {
            return 0;
        }
        if (connections.length < n - 1) {
            return -1;
        }
        int[][] edges = connections.clone();
        Arrays.sort(edges, (a, b) -> Integer.compare(a[2], b[2]));

        int[] parent = new int[n + 1];
        int[] size = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            parent[i] = i;
            size[i] = 1;
        }

        int total = 0;
        int components = n;
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
                    return total;
                }
            }
        }
        return -1;
    }
}
