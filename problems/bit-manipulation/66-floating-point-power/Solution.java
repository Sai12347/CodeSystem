class Solution {
    public double myPow(double x, int n) {
        long exp = n;
        double base = x;
        if (exp < 0L) {
            base = 1.0 / base;
            exp = -exp;
        }
        double res = 1.0;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) {
                res *= base;
            }
            base *= base;
            exp >>= 1;
        }
        return res;
    }
}
