class Solution {
    public int[] dailyTemperatures(int[] temperatures) {
        int n = temperatures.length;
        int[] ans = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            int t = temperatures[i];
            while (!stack.isEmpty() && temperatures[stack.peek()] < t) {
                int prev = stack.pop();
                ans[prev] = i - prev;
            }
            stack.push(i);
        }
        return ans;
    }
}
