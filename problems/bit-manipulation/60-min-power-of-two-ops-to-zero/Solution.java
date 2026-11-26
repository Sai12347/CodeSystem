class Solution {
    public int minOpsToZero(int n) {
        long x = n;
        int ops = 0;
        while (x > 0L) {
            long low = x & -x;
            if ((x & (low << 1)) != 0L) {
                x += low;
            } else {
                x -= low;
            }
            ops++;
        }
        return ops;
    }
}
