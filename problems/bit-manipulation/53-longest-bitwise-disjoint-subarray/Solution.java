class Solution {
    public int longestDisjointSubarray(int[] nums) {
        int used = 0;
        int left = 0;
        int best = 0;
        for (int right = 0; right < nums.length; right++) {
            int x = nums[right];
            while ((used & x) != 0) {
                used ^= nums[left++];
            }
            used |= x;
            int cur = right - left + 1;
            if (cur > best) best = cur;
        }
        return best;
    }
}
