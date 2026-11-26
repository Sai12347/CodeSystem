class Solution {
    public int[] canSeePersonsCount(int[] heights) {
        int n = heights.length;
        int[] ans = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = n - 1; i >= 0; i--) {
            int h = heights[i];
            int visible = 0;
            while (!stack.isEmpty() && stack.peek() < h) {
                stack.pop();
                visible++;
            }
            if (!stack.isEmpty()) {
                visible++;
            }
            ans[i] = visible;
            stack.push(h);
        }
        return ans;
    }
}
