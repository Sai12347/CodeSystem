class Solution {
    public String fractionAddition(String expression) {
        long num = 0, den = 1;
        int i = 0, n = expression.length();
        while (i < n) {
            int sign = 1;
            if (expression.charAt(i) == '+' || expression.charAt(i) == '-') {
                sign = expression.charAt(i++) == '-' ? -1 : 1;
            }
            long a = 0;
            while (i < n && Character.isDigit(expression.charAt(i))) {
                a = a * 10 + (expression.charAt(i++) - '0');
            }
            i++; // skip '/'
            long b = 0;
            while (i < n && Character.isDigit(expression.charAt(i))) {
                b = b * 10 + (expression.charAt(i++) - '0');
            }
            num = num * b + sign * a * den;
            den *= b;
            long g = gcd(Math.abs(num), den);
            num /= g;
            den /= g;
        }
        return num + "/" + den;
    }
    private long gcd(long a, long b) {
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;
    }
}
