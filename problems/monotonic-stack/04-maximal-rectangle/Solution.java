class Solution {
    public int maximalRectangle(char[][] matrix) {
        if (matrix.length == 0 || matrix[0].length == 0) {
            return 0;
        }
        int cols = matrix[0].length;
        int[] heights = new int[cols];
        int best = 0;
        Deque<Integer> stack = new ArrayDeque<>();
        for (char[] row : matrix) {
            for (int c = 0; c < cols; c++) {
                heights[c] = (row[c] == '1') ? heights[c] + 1 : 0;
            }
            stack.clear();
            for (int i = 0; i <= cols; i++) {
                int cur = (i == cols) ? 0 : heights[i];
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
        }
        return best;
    }
}
