class Adapter {
    private static long[] expectedKSums(int[] nums1, int[] nums2, int target) {
        PriorityQueue<long[]> minHeap = new PriorityQueue<>(Comparator.comparingLong(a -> a[0]));
        int limit = Math.min(nums1.length, target);
        for (int i = 0; i < limit; i++) {
            minHeap.offer(new long[]{(long) nums1[i] + nums2[0], i, 0});
        }
        long[] sums = new long[target];
        int idx = 0;
        while (!minHeap.isEmpty() && idx < target) {
            long[] top = minHeap.poll();
            sums[idx++] = top[0];
            int i = (int) top[1], j = (int) top[2];
            if (j + 1 < nums2.length) {
                minHeap.offer(new long[]{(long) nums1[i] + nums2[j + 1], i, j + 1});
            }
        }
        return sums;
    }

    public static Object run(Map<String, Object> inp) {
        int[] nums1 = (int[]) Judge.convert(inp.get("nums1"), "int[]");
        int[] nums2 = (int[]) Judge.convert(inp.get("nums2"), "int[]");
        int k = ((Number) inp.get("k")).intValue();
        List<List<Integer>> res = new Solution().kSmallestPairs(nums1.clone(), nums2.clone(), k);
        long totalPairs = (long) nums1.length * nums2.length;
        int target = (int) Math.min(k, totalPairs);
        if (res == null) {
            return "Expected non-null List<List<Integer>>, got null";
        }
        if (res.size() != target) {
            return "Expected " + target + " pairs, got " + res.size();
        }
        Map<Integer, Integer> cnt1 = new HashMap<>();
        for (int x : nums1) cnt1.merge(x, 1, Integer::sum);
        Map<Integer, Integer> cnt2 = new HashMap<>();
        for (int y : nums2) cnt2.merge(y, 1, Integer::sum);
        Map<Long, Integer> pairCnt = new HashMap<>();
        long[] gotSums = new long[target];
        for (int idx = 0; idx < target; idx++) {
            List<Integer> p = res.get(idx);
            if (p == null || p.size() != 2 || p.get(0) == null || p.get(1) == null) {
                return "Element at index " + idx + " is not a valid 2-integer pair";
            }
            int u = p.get(0), v = p.get(1);
            int c1 = cnt1.getOrDefault(u, 0);
            int c2 = cnt2.getOrDefault(v, 0);
            if (c1 == 0 || c2 == 0) {
                return "Pair [" + u + ", " + v + "] uses values not present in nums1/nums2";
            }
            long key = (((long) u) << 32) ^ (v & 0xffffffffL);
            int used = pairCnt.merge(key, 1, Integer::sum);
            if (used > (long) c1 * c2) {
                return "Pair [" + u + ", " + v + "] appears more times than distinct index pairs allow";
            }
            gotSums[idx] = (long) u + v;
        }
        Arrays.sort(gotSums);
        long[] expSums = expectedKSums(nums1, nums2, target);
        if (!Arrays.equals(gotSums, expSums)) {
            return "Returned pair sums do not match the k smallest sums";
        }
        return true;
    }
}
