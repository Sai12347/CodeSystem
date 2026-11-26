class Solution {
    public List<List<Integer>> kSmallestPairs(int[] nums1, int[] nums2, int k) {
        List<List<Integer>> res = new ArrayList<>();
        if (nums1.length == 0 || nums2.length == 0 || k <= 0) return res;
        PriorityQueue<long[]> minHeap = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
        int limit = Math.min(nums1.length, k);
        for (int i = 0; i < limit; i++) {
            minHeap.offer(new long[]{(long) nums1[i] + nums2[0], i, 0});
        }
        while (!minHeap.isEmpty() && res.size() < k) {
            long[] top = minHeap.poll();
            int i = (int) top[1], j = (int) top[2];
            res.add(Arrays.asList(nums1[i], nums2[j]));
            if (j + 1 < nums2.length) {
                minHeap.offer(new long[]{(long) nums1[i] + nums2[j + 1], i, j + 1});
            }
        }
        return res;
    }
}
