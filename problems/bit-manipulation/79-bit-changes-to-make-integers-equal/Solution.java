class Solution {
    public int minBitChanges(int n, int k) {
        if ((n & k) != k) return -1;
        return Integer.bitCount(n ^ k);
    }
}
