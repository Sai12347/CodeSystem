class Solution {
    public int findUnsortedSubarray(int[] nums) {
        int n = nums.length;
        int right = -1;
        int maxSeen = nums[0];
        for (int i = 1; i < n; i++) {
            if (nums[i] < maxSeen) {
                right = i;
            } else {
                maxSeen = nums[i];
            }
        }
        if (right == -1) {
            return 0;
        }

        int left = n;
        int minSeen = nums[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            if (nums[i] > minSeen) {
                left = i;
            } else {
                minSeen = nums[i];
            }
        }
        return right - left + 1;
    }
}
