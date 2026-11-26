class Solution {
    public int findMaximumXOR(int[] nums) {
        int maxVal = 0;
        for (int num : nums) {
            if (num > maxVal) {
                maxVal = num;
            }
        }
        if (maxVal == 0) {
            return 0;
        }
        int highBit = 31 - Integer.numberOfLeadingZeros(maxVal);
        int maxNodes = nums.length * (highBit + 1) + 2;
        int[][] next = new int[maxNodes][2];
        int nodeCount = 1;
        int best = 0;

        for (int num : nums) {
            int cur = 0;
            int xorCur = 0;
            int curXor = 0;
            for (int b = highBit; b >= 0; b--) {
                int bit = (num >>> b) & 1;
                if (next[cur][bit] == 0) {
                    next[cur][bit] = nodeCount++;
                }
                cur = next[cur][bit];

                int toggled = bit ^ 1;
                if (next[xorCur][toggled] != 0) {
                    curXor |= (1 << b);
                    xorCur = next[xorCur][toggled];
                } else {
                    xorCur = next[xorCur][bit];
                }
            }
            if (curXor > best) {
                best = curXor;
            }
        }
        return best;
    }
}
