class Solution {
    public int countPrimeSetBits(int left, int right) {
        int primeMask = 665772;
        int ans = 0;
        for (int x = left; x <= right; x++) {
            if (((primeMask >>> Integer.bitCount(x)) & 1) == 1) {
                ans++;
            }
        }
        return ans;
    }
}
