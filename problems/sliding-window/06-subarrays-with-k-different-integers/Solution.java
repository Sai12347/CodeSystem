class Solution {
    public int subarraysWithKDistinct(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    private int atMost(int[] nums, int limit) {
        if (limit <= 0) {
            return 0;
        }
        Map<Integer, Integer> counts = new HashMap<>();
        int left = 0;
        int total = 0;
        for (int right = 0; right < nums.length; right++) {
            int v = nums[right];
            counts.put(v, counts.getOrDefault(v, 0) + 1);
            while (counts.size() > limit) {
                int lv = nums[left];
                int c = counts.get(lv) - 1;
                if (c == 0) {
                    counts.remove(lv);
                } else {
                    counts.put(lv, c);
                }
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }
}
