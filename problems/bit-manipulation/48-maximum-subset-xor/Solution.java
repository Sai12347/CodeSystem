class Solution {
    public int maxSubsetXor(int[] nums) {
        int[] basis = new int[31];
        for (int x : nums) {
            for (int b = 30; b >= 0; b--) {
                if (((x >> b) & 1) != 0) {
                    if (basis[b] == 0) {
                        basis[b] = x;
                        break;
                    }
                    x ^= basis[b];
                }
            }
        }
        int ans = 0;
        for (int b = 30; b >= 0; b--) {
            if ((ans ^ basis[b]) > ans) {
                ans ^= basis[b];
            }
        }
        return ans;
    }
}
