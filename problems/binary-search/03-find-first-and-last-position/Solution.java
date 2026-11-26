class Solution {
    public int[] searchRange(int[] nums, int target) {
        int first = findBound(nums, target, true);
        if (first == nums.length || nums[first] != target) {
            return new int[]{-1, -1};
        }
        int last = findBound(nums, target, false) - 1;
        return new int[]{first, last};
    }

    private int findBound(int[] nums, int target, boolean isLower) {
        int left = 0;
        int right = nums.length;
        while (left < right) {
            int mid = left + (right - left) / 2;
            if (isLower ? nums[mid] < target : nums[mid] <= target) {
                left = mid + 1;
            } else {
                right = mid;
            }
        }
        return left;
    }
}
