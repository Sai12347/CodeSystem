class Solution {
    public int maxWidthRamp(int[] nums) {
        int[] stack = new int[nums.length]; int size = 0;
        for (int i = 0; i < nums.length; i++) if (size == 0 || nums[i] < nums[stack[size - 1]]) stack[size++] = i;
        int best = 0;
        for (int j = nums.length - 1; j >= 0; j--) while (size > 0 && nums[stack[size - 1]] <= nums[j]) best = Math.max(best, j - stack[--size]);
        return best;
    }
}
