class Solution {
    public int[] evenOddBit(int n) {
        return new int[]{Integer.bitCount(n & 0x55555555), Integer.bitCount(n & 0x2AAAAAAA)};
    }
}
