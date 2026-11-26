class Solution {
    public int maxTurbulenceSize(int[] nums) {
        int up = 1, down = 1, best = 1;
        for (int i = 1; i < nums.length; i++) { if (nums[i] > nums[i-1]) { up = down + 1; down = 1; } else if (nums[i] < nums[i-1]) { down = up + 1; up = 1; } else { up = 1; down = 1; } best = Math.max(best, Math.max(up, down)); }
        return best;
    }
}
