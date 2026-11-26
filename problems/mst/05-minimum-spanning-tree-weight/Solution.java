class Solution {
    public long minimumSpanningTreeWeight(int n, int[][] edges) {
        if (n <= 1) {
            return 0L;
        }
        List<List<int[]>> adj = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            adj.add(new ArrayList<>());
        }
        for (int[] e : edges) {
            int u = e[0];
            int v = e[1];
            int w = e[2];
            if (u != v) {
                adj.get(u).add(new int[]{v, w});
                adj.get(v).add(new int[]{u, w});
            }
        }

        boolean[] visited = new boolean[n];
        PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
        pq.offer(new int[]{0, 0});

        long total = 0L;
        int visitedCount = 0;

        while (!pq.isEmpty() && visitedCount < n) {
            int[] cur = pq.poll();
            int w = cur[0];
            int u = cur[1];
            if (visited[u]) {
                continue;
            }
            visited[u] = true;
            total += w;
            visitedCount++;
            for (int[] nxt : adj.get(u)) {
                int v = nxt[0];
                if (!visited[v]) {
                    pq.offer(new int[]{nxt[1], v});
                }
            }
        }
        return visitedCount == n ? total : -1L;
    }
}
