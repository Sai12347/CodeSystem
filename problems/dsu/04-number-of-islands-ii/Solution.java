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

    public List<Integer> numIslands2(int m, int n, int[][] positions) {
        parent = new int[m * n];
        rank = new int[m * n];
        Arrays.fill(parent, -1);

        int count = 0;
        List<Integer> ans = new ArrayList<>(positions.length);
        int[][] dirs = {{-1, 0}, {1, 0}, {0, -1}, {0, 1}};

        for (int[] pos : positions) {
            int r = pos[0], c = pos[1];
            int idx = r * n + c;
            if (parent[idx] != -1) {
                ans.add(count);
                continue;
            }
            parent[idx] = idx;
            count++;
            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n) {
                    int nidx = nr * n + nc;
                    if (parent[nidx] != -1) {
                        int ra = find(idx), rb = find(nidx);
                        if (ra != rb) {
                            if (rank[ra] < rank[rb]) {
                                int tmp = ra;
                                ra = rb;
                                rb = tmp;
                            }
                            parent[rb] = ra;
                            if (rank[ra] == rank[rb]) rank[ra]++;
                            count--;
                        }
                    }
                }
            }
            ans.add(count);
        }
        return ans;
    }
}
