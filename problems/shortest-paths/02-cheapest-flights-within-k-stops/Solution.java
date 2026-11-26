class Solution {
    public int findCheapestPrice(int n, int[][] flights, int src, int dst, int k) {
        final int INF = Integer.MAX_VALUE / 2;
        int[] dist = new int[n];
        Arrays.fill(dist, INF);
        dist[src] = 0;

        for (int i = 0; i <= k; i++) {
            int[] next = Arrays.copyOf(dist, n);
            boolean updated = false;
            for (int[] f : flights) {
                int u = f[0], v = f[1], price = f[2];
                if (dist[u] != INF && dist[u] + price < next[v]) {
                    next[v] = dist[u] + price;
                    updated = true;
                }
            }
            dist = next;
            if (!updated) {
                break;
            }
        }

        return dist[dst] >= INF ? -1 : dist[dst];
    }
}
