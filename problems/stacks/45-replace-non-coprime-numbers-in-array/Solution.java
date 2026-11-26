class Solution {
    public List<Integer> replaceNonCoprimes(int[] nums) {
        List<Integer> stack = new ArrayList<>();
        for (int x : nums) {
            long cur = x;
            while (!stack.isEmpty()) {
                long top = stack.get(stack.size() - 1);
                long g = gcd(top, cur);
                if (g == 1) break;
                stack.remove(stack.size() - 1);
                cur = (top / g) * cur;
            }
            stack.add((int) cur);
        }
        return stack;
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
