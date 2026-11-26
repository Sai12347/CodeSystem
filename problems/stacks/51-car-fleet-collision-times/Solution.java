class Solution {
    public double[] getCollisionTimes(int[][] cars) {
        int n = cars.length;
        double[] ans = new double[n];
        Arrays.fill(ans, -1.0);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = n - 1; i >= 0; i--) {
            int p = cars[i][0], s = cars[i][1];
            while (!stack.isEmpty()) {
                int j = stack.peek();
                int pj = cars[j][0], sj = cars[j][1];
                if (s <= sj || (ans[j] > 0 && (double) (pj - p) / (s - sj) >= ans[j])) {
                    stack.pop();
                } else {
                    break;
                }
            }
            if (!stack.isEmpty()) {
                int j = stack.peek();
                ans[i] = (double) (cars[j][0] - p) / (s - cars[j][1]);
            }
            stack.push(i);
        }
        return ans;
    }
}
