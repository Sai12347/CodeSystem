class Solution {
    public boolean hasAlternatingBits(int n) {
        long x = (long) n ^ (n >>> 1);
        return (x & (x + 1)) == 0;
    }
}
