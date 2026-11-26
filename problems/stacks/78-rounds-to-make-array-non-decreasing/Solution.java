class Solution {
    public int totalRounds(int[] nums) {
        Deque<int[]> stack = new ArrayDeque<>();
        int ans = 0;
        for (int x : nums) {
            int rounds = 0;
            while (!stack.isEmpty() && stack.peek()[0] <= x) {
                rounds = Math.max(rounds, stack.pop()[1]);
            }
            if (!stack.isEmpty()) {
                rounds++;
            } else {
                rounds = 0;
            }
            if (rounds > ans) ans = rounds;
            stack.push(new int[]{x, rounds});
        }
        return ans;
    }
}
