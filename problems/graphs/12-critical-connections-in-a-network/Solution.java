class Solution {
    public List<List<Integer>> criticalConnections(int n, List<List<Integer>> connections) {
        List<List<Integer>> adj = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        for (List<Integer> edge : connections) {
            int u = edge.get(0);
            int v = edge.get(1);
            adj.get(u).add(v);
            adj.get(v).add(u);
        }

        int[] disc = new int[n];
        int[] low = new int[n];
        Arrays.fill(disc, -1);
        List<List<Integer>> bridges = new ArrayList<>();
        int timer = 0;

        int[] stackNode = new int[n];
        int[] stackParent = new int[n];
        int[] stackIdx = new int[n];

        for (int start = 0; start < n; start++) {
            if (disc[start] != -1) continue;
            disc[start] = low[start] = timer++;
            int top = 0;
            stackNode[0] = start;
            stackParent[0] = -1;
            stackIdx[0] = 0;

            while (top >= 0) {
                int u = stackNode[top];
                int parent = stackParent[top];
                int idx = stackIdx[top];
                List<Integer> nbrs = adj.get(u);
                if (idx < nbrs.size()) {
                    stackIdx[top] = idx + 1;
                    int v = nbrs.get(idx);
                    if (v == parent) continue;
                    if (disc[v] == -1) {
                        disc[v] = low[v] = timer++;
                        top++;
                        stackNode[top] = v;
                        stackParent[top] = u;
                        stackIdx[top] = 0;
                    } else if (disc[v] < low[u]) {
                        low[u] = disc[v];
                    }
                } else {
                    top--;
                    if (parent != -1) {
                        if (low[u] < low[parent]) {
                            low[parent] = low[u];
                        }
                        if (low[u] > disc[parent]) {
                            bridges.add(Arrays.asList(parent, u));
                        }
                    }
                }
            }
        }
        return bridges;
    }
}
