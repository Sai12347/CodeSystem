class Solution {
    public int largestRectangleArea(int[] heights) {
        int n = heights.length;
        Deque<Integer> stack = new ArrayDeque<>();
        int best = 0;
        for (int i = 0; i <= n; i++) {
            int cur = (i == n) ? 0 : heights[i];
            while (!stack.isEmpty() && heights[stack.peek()] > cur) {
                int h = heights[stack.pop()];
                int left = stack.isEmpty() ? -1 : stack.peek();
                int area = h * (i - left - 1);
                if (area > best) {
                    best = area;
                }
            }
            stack.push(i);
        }
        return best;
    }
}
