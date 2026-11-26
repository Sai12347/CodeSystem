class Solution {
    public int[] smallestRange(List<List<Integer>> nums) {
        int k = nums.size();
        PriorityQueue<int[]> minHeap = new PriorityQueue<>(Comparator.comparingInt(a -> a[0]));
        int curMax = Integer.MIN_VALUE;
        for (int i = 0; i < k; i++) {
            int val = nums.get(i).get(0);
            minHeap.offer(new int[]{val, i, 0});
            if (val > curMax) curMax = val;
        }
        int bestL = minHeap.peek()[0];
        int bestR = curMax;
        while (true) {
            int[] top = minHeap.poll();
            int curMin = top[0], r = top[1], c = top[2];
            if (curMax - curMin < bestR - bestL || (curMax - curMin == bestR - bestL && curMin < bestL)) {
                bestL = curMin;
                bestR = curMax;
            }
            List<Integer> row = nums.get(r);
            if (c + 1 == row.size()) {
                break;
            }
            int nxt = row.get(c + 1);
            if (nxt > curMax) curMax = nxt;
            minHeap.offer(new int[]{nxt, r, c + 1});
        }
        return new int[]{bestL, bestR};
    }
}
