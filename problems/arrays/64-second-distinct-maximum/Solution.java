class Solution {
    public int secondDistinctMaximum(int[] nums) {
        long first = Long.MIN_VALUE, second = Long.MIN_VALUE; boolean haveFirst = false, haveSecond = false;
        for (int x : nums) { if (haveFirst && x == first || haveSecond && x == second) continue; if (!haveFirst || x > first) { second = first; haveSecond = haveFirst; first = x; haveFirst = true; } else if (!haveSecond || x > second) { second = x; haveSecond = true; } }
        return haveSecond ? (int) second : -1;
    }
}
