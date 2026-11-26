class Solution {
    public int trapRainWater(int[][] heightMap) {
        int m = heightMap.length, n = heightMap[0].length;
        if (m <= 2 || n <= 2) return 0;
        boolean[][] visited = new boolean[m][n];
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        for (int r = 0; r < m; r++) {
            visited[r][0] = true;
            visited[r][n - 1] = true;
            minHeap.offer(new int[]{heightMap[r][0], r, 0});
            minHeap.offer(new int[]{heightMap[r][n - 1], r, n - 1});
        }
        for (int c = 1; c < n - 1; c++) {
            visited[0][c] = true;
            visited[m - 1][c] = true;
            minHeap.offer(new int[]{heightMap[0][c], 0, c});
            minHeap.offer(new int[]{heightMap[m - 1][c], m - 1, c});
        }
        int water = 0;
        int[][] dirs = {{1, 0}, {-1, 0}, {0, 1}, {0, -1}};
        while (!minHeap.isEmpty()) {
            int[] cur = minHeap.poll();
            int h = cur[0], r = cur[1], c = cur[2];
            for (int[] d : dirs) {
                int nr = r + d[0], nc = c + d[1];
                if (nr >= 0 && nr < m && nc >= 0 && nc < n && !visited[nr][nc]) {
                    visited[nr][nc] = true;
                    int nh = heightMap[nr][nc];
                    if (nh < h) {
                        water += h - nh;
                        minHeap.offer(new int[]{h, nr, nc});
                    } else {
                        minHeap.offer(new int[]{nh, nr, nc});
                    }
                }
            }
        }
        return water;
    }
}
