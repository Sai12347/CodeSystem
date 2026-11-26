class Solution {
    public int smallestAllSetBits(int n) {
        int bits = 32 - Integer.numberOfLeadingZeros(n);
        return (1 << bits) - 1;
    }
}
