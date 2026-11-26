class Solution {
    public int findIntegers(int n) {
        int[] fib = new int[32];
        fib[0] = 1;
        fib[1] = 2;
        for (int i = 2; i < 32; i++) {
            fib[i] = fib[i - 1] + fib[i - 2];
        }
        int ans = 0;
        int prevBit = 0;
        for (int b = 30; b >= 0; b--) {
            if (((n >> b) & 1) != 0) {
                ans += fib[b];
                if (prevBit == 1) return ans;
                prevBit = 1;
            } else {
                prevBit = 0;
            }
        }
        return ans + 1;
    }
}
