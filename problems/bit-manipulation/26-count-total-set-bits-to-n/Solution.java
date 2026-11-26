class Solution {
    public long countTotalSetBits(long n) {
        long m = n + 1;
        long total = 0;
        long half = 1;
        while (half <= n) {
            long cycle = half << 1;
            total += (m / cycle) * half;
            long rem = m % cycle;
            if (rem > half) {
                total += rem - half;
            }
            half = cycle;
        }
        return total;
    }
}
