class Solution {
    public int connectSticks(int[] sticks) {
        if (sticks.length <= 1) return 0;
        PriorityQueue<Integer> minHeap = new PriorityQueue<>(sticks.length);
        for (int s : sticks) {
            minHeap.offer(s);
        }
        int total = 0;
        while (minHeap.size() > 1) {
            int merged = minHeap.poll() + minHeap.poll();
            total += merged;
            minHeap.offer(merged);
        }
        return total;
    }
}
