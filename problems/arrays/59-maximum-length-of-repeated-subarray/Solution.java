class Solution {
    public int findLength(int[] nums1, int[] nums2) {
        if (nums2.length > nums1.length) return findLength(nums2, nums1);
        int[] dp = new int[nums2.length + 1]; int best = 0;
        for (int x : nums1) for (int j = nums2.length - 1; j >= 0; j--) { dp[j + 1] = x == nums2[j] ? dp[j] + 1 : 0; best = Math.max(best, dp[j + 1]); }
        return best;
    }
}
