class Solution {
    public int minCostConnectPoints(int[][] points) {
        int n = points.length;
        if (n <= 1) {
            return 0;
        }
        boolean[] inMst = new boolean[n];
        int[] minDist = new int[n];
        Arrays.fill(minDist, Integer.MAX_VALUE);
        minDist[0] = 0;

        int totalCost = 0;
        for (int iter = 0; iter < n; iter++) {
            int u = -1;
            int best = Integer.MAX_VALUE;
            for (int i = 0; i < n; i++) {
                if (!inMst[i] && minDist[i] < best) {
                    best = minDist[i];
                    u = i;
                }
            }
            inMst[u] = true;
            totalCost += best;
            int ux = points[u][0];
            int uy = points[u][1];
            for (int v = 0; v < n; v++) {
                if (!inMst[v]) {
                    int d = Math.abs(ux - points[v][0]) + Math.abs(uy - points[v][1]);
                    if (d < minDist[v]) {
                        minDist[v] = d;
                    }
                }
            }
        }
        return totalCost;
    }
}
