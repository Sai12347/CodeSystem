class Solution {
    public int kthSmallestSubsetXor(int[] nums, long k) {
        int[] basis = new int[30];
        for (int x : nums) {
            int v = x;
            for (int b = 29; b >= 0; b--) {
                if (((v >> b) & 1) != 0) {
                    if (basis[b] == 0) {
                        basis[b] = v;
                        break;
                    }
                    v ^= basis[b];
                }
            }
        }
        for (int b = 0; b < 30; b++) {
            if (basis[b] != 0) {
                for (int high = b + 1; high < 30; high++) {
                    if (((basis[high] >> b) & 1) != 0) {
                        basis[high] ^= basis[b];
                    }
                }
            }
        }
        int[] vecs = new int[30];
        int r = 0;
        for (int b = 0; b < 30; b++) {
            if (basis[b] != 0) vecs[r++] = basis[b];
        }
        if (k > (1L << r)) return -1;
        long idx = k - 1L;
        int ans = 0;
        for (int i = 0; i < r; i++) {
            if (((idx >> i) & 1L) != 0L) {
                ans ^= vecs[i];
            }
        }
        return ans;
    }
}
