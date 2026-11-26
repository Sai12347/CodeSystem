class Solution {
    public int minimumEqualDistance(int[] nums) {
        Map<Integer, Integer> last = new HashMap<>();
        int best = nums.length + 1;
        for (int i = 0; i < nums.length; i++) { Integer prev = last.put(nums[i], i); if (prev != null) best = Math.min(best, i - prev); }
        return best <= nums.length ? best : -1;
    }
}
