class Solution {
    public int minAlignedBlocks(long start, long n) {
        int blocks = 0;
        long cur = start;
        long rem = n;
        while (rem > 0L) {
            long maxStep = 1L << (63 - Long.numberOfLeadingZeros(rem));
            long step = (cur == 0L) ? maxStep : Math.min(cur & -cur, maxStep);
            cur += step;
            rem -= step;
            blocks++;
        }
        return blocks;
    }
}
