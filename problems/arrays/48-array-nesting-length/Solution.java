class Solution {
    public int arrayNesting(int[] nums) {
        boolean[] seen = new boolean[nums.length]; int best = 0;
        for (int start = 0; start < nums.length; start++) { int length = 0, i = start; while (!seen[i]) { seen[i] = true; length++; i = nums[i]; } best = Math.max(best, length); }
        return best;
    }
}
