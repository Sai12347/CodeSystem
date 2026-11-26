class Solution {
    public int minMeetingRooms(int[][] intervals) {
        Arrays.sort(intervals, (a, b) -> Integer.compare(a[0], b[0]));
        PriorityQueue<Integer> minHeap = new PriorityQueue<>();
        for (int[] iv : intervals) {
            if (!minHeap.isEmpty() && minHeap.peek() <= iv[0]) {
                minHeap.poll();
            }
            minHeap.offer(iv[1]);
        }
        return minHeap.size();
    }
}
