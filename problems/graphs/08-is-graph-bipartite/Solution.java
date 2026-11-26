class Solution {
    public boolean isBipartite(int[][] graph) {
        int n = graph.length;
        int[] color = new int[n];
        ArrayDeque<Integer> queue = new ArrayDeque<>();

        for (int start = 0; start < n; start++) {
            if (color[start] != 0) continue;
            color[start] = 1;
            queue.offer(start);
            while (!queue.isEmpty()) {
                int u = queue.poll();
                int nextColor = -color[u];
                for (int v : graph[u]) {
                    if (color[v] == 0) {
                        color[v] = nextColor;
                        queue.offer(v);
                    } else if (color[v] != nextColor) {
                        return false;
                    }
                }
            }
        }
        return true;
    }
}
