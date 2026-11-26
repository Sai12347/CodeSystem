class Solution {
    public long countAndGreaterThanXor(int[] nums) {
        long[] buckets = new long[31];
        for (int x : nums) {
            buckets[31 - Integer.numberOfLeadingZeros(x)]++;
        }
        long ans = 0L;
        for (long c : buckets) {
            ans += c * (c - 1L) / 2L;
        }
        return ans;
    }
}
