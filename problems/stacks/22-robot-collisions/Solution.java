class Solution {
    public List<Integer> survivedRobotsHealths(int[] positions, int[] healths, String directions) {
        int n = positions.length;
        Integer[] order = new Integer[n];
        int[] hp = Arrays.copyOf(healths, n);
        for (int i = 0; i < n; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> Integer.compare(positions[a], positions[b]));
        Deque<Integer> stack = new ArrayDeque<>();
        for (int idx : order) {
            if (directions.charAt(idx) == 'R') {
                stack.push(idx);
            } else {
                while (!stack.isEmpty() && hp[idx] > 0) {
                    int top = stack.peek();
                    if (hp[top] < hp[idx]) {
                        stack.pop();
                        hp[top] = 0;
                        hp[idx]--;
                    } else if (hp[top] > hp[idx]) {
                        hp[top]--;
                        hp[idx] = 0;
                    } else {
                        stack.pop();
                        hp[top] = 0;
                        hp[idx] = 0;
                    }
                }
            }
        }
        List<Integer> ans = new ArrayList<>();
        for (int h : hp) {
            if (h > 0) ans.add(h);
        }
        return ans;
    }
}
