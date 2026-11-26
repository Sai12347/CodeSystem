class Solution {
    public boolean canSortBySetBits(int[] nums) {
        int prevMax = 0;
        int curPop = Integer.bitCount(nums[0]);
        int curMin = nums[0];
        int curMax = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            int p = Integer.bitCount(x);
            if (p == curPop) {
                if (x < curMin) curMin = x;
                if (x > curMax) curMax = x;
            } else {
                if (curMin < prevMax) return false;
                prevMax = curMax;
                curPop = p;
                curMin = x;
                curMax = x;
            }
        }
        return curMin >= prevMax;
    }
}
