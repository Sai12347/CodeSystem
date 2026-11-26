class Solution {
    public int numberOfSubarrays(int[] nums, int k) {
        return atMost(nums, k) - atMost(nums, k - 1);
    }

    private int atMost(int[] nums, int goal) {
        if (goal < 0) {
            return 0;
        }
        int left = 0;
        int odds = 0;
        int total = 0;
        for (int right = 0; right < nums.length; right++) {
            odds += nums[right] & 1;
            while (odds > goal) {
                odds -= nums[left] & 1;
                left++;
            }
            total += right - left + 1;
        }
        return total;
    }
}
