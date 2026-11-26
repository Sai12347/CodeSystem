class Solution {
    private int step(int x) {
        int total = 0;
        while (x > 0) {
            int d = x % 10;
            total += d * d;
            x /= 10;
        }
        return total;
    }

    public boolean isHappy(int n) {
        int slow = n;
        int fast = step(n);
        while (fast != 1 && slow != fast) {
            slow = step(slow);
            fast = step(step(fast));
        }
        return fast == 1;
    }
}
