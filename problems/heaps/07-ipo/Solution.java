class Solution {
    public int findMaximizedCapital(int k, int w, int[] profits, int[] capital) {
        int n = profits.length;
        int[][] projects = new int[n][2];
        for (int i = 0; i < n; i++) {
            projects[i][0] = capital[i];
            projects[i][1] = profits[i];
        }
        Arrays.sort(projects, Comparator.comparingInt(a -> a[0]));
        PriorityQueue<Integer> maxHeap = new PriorityQueue<>(Collections.reverseOrder());
        int idx = 0;
        int steps = Math.min(k, n);
        for (int i = 0; i < steps; i++) {
            while (idx < n && projects[idx][0] <= w) {
                maxHeap.offer(projects[idx][1]);
                idx++;
            }
            if (maxHeap.isEmpty()) {
                break;
            }
            w += maxHeap.poll();
        }
        return w;
    }
}
