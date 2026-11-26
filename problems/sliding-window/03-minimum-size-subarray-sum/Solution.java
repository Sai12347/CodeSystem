class Solution {
    public int minSubArrayLen(int target, int[] nums) {
        int left = 0;
        long windowSum = 0;
        int best = nums.length + 1;
        for (int right = 0; right < nums.length; right++) {
            windowSum += nums[right];
            while (windowSum >= target) {
                int len = right - left + 1;
                if (len < best) {
                    best = len;
                }
                windowSum -= nums[left];
                left++;
            }
        }
        return best > nums.length ? 0 : best;
    }
}
