class Solution {
    public int kthSmallestRowSum(int[][] mat, int k) {
        int m = mat.length, n = mat[0].length;
        int len = Math.min(n, k);
        int[] cur = Arrays.copyOf(mat[0], len);
        for (int r = 1; r < m; r++) {
            int[] row = mat[r];
            PriorityQueue<int[]> pq = new PriorityQueue<>((a, b) -> Integer.compare(a[0], b[0]));
            for (int i = 0; i < cur.length; i++) {
                pq.offer(new int[]{cur[i] + row[0], i, 0});
            }
            int limit = Math.min(k, cur.length * n);
            int[] nxt = new int[limit];
            int idx = 0;
            while (!pq.isEmpty() && idx < limit) {
                int[] top = pq.poll();
                nxt[idx++] = top[0];
                int i = top[1], j = top[2];
                if (j + 1 < n) {
                    pq.offer(new int[]{cur[i] + row[j + 1], i, j + 1});
                }
            }
            cur = nxt;
        }
        return cur[k - 1];
    }
}
