class Solution {
    public int getMaxLen(int[] nums) {
        int positive = 0, negative = 0, best = 0;
        for (int x : nums) { if (x == 0) { positive = 0; negative = 0; } else if (x > 0) { positive++; if (negative > 0) negative++; } else { int oldPositive = positive; positive = negative > 0 ? negative + 1 : 0; negative = oldPositive + 1; } best = Math.max(best, positive); }
        return best;
    }
}
