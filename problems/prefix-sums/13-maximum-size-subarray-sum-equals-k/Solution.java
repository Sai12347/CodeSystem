class Solution {
    public int maxSubArrayLen(int[] nums, int k) {
        Map<Long, Integer> firstSeen = new HashMap<>();
        firstSeen.put(0L, -1);
        long prefix = 0L;
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            prefix += nums[i];
            Integer prev = firstSeen.get(prefix - k);
            if (prev != null) {
                int len = i - prev;
                if (len > best) {
                    best = len;
                }
            }
            firstSeen.putIfAbsent(prefix, i);
        }
        return best;
    }
}
