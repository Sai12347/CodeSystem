class Solution {
    public int dominantIndex(int[] nums) {
        int best = -1, second = -1, index = -1;
        for (int i = 0; i < nums.length; i++) { int x = nums[i]; if (x > best) { second = best; best = x; index = i; } else if (x > second) second = x; }
        return best >= 2L * second ? index : -1;
    }
}
