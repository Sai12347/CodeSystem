class Solution {
    public int sumSubarrayMins(int[] arr) {
        final long MOD = 1_000_000_007L;
        int n = arr.length;
        Deque<Integer> stack = new ArrayDeque<>();
        long total = 0;
        for (int i = 0; i <= n; i++) {
            int cur = (i == n) ? 0 : arr[i];
            while (!stack.isEmpty() && arr[stack.peek()] >= cur) {
                int mid = stack.pop();
                int left = stack.isEmpty() ? -1 : stack.peek();
                long contrib = ((long) arr[mid] * (mid - left)) % MOD;
                contrib = (contrib * (i - mid)) % MOD;
                total = (total + contrib) % MOD;
            }
            stack.push(i);
        }
        return (int) total;
    }
}
