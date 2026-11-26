class Solution {
    public int maximumUniqueSubarray(int[] nums) {
        Map<Integer, Integer> last = new HashMap<>(); int left = 0, best = 0; long sum = 0;
        for (int right = 0; right < nums.length; right++) {
            Integer prev = last.get(nums[right]); if (prev != null && prev >= left) { while (left <= prev) sum -= nums[left++]; }
            last.put(nums[right], right); sum += nums[right]; best = Math.max(best, (int) sum);
        }
        return best;
    }
}
