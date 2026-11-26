class Solution {
    public int kthSmallest(int[][] matrix, int k) {
        int n = matrix.length;
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        int limit = Math.min(n, k);
        for (int r = 0; r < limit; r++) {
            minHeap.offer(new int[]{matrix[r][0], r, 0});
        }
        int val = 0;
        for (int i = 0; i < k; i++) {
            int[] cur = minHeap.poll();
            val = cur[0];
            int r = cur[1], c = cur[2];
            if (c + 1 < n) {
                minHeap.offer(new int[]{matrix[r][c + 1], r, c + 1});
            }
        }
        return val;
    }
}
