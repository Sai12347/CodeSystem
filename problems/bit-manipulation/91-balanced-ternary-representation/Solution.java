class Solution {
    public String toBalancedTernary(long n) {
        if (n == 0L) return "0";
        StringBuilder sb = new StringBuilder();
        long x = n;
        while (x != 0L) {
            long r = ((x % 3L) + 3L) % 3L;
            if (r == 0L) {
                sb.append('0');
                x /= 3L;
            } else if (r == 1L) {
                sb.append('+');
                x = (x - 1L) / 3L;
            } else {
                sb.append('-');
                x = (x + 1L) / 3L;
            }
        }
        return sb.reverse().toString();
    }
}
