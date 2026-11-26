class Solution {
    public int minFlipsForOr(int a, int b, int c) {
        int diff = (a | b) ^ c;
        return Integer.bitCount(diff) + Integer.bitCount(a & b & diff);
    }
}
