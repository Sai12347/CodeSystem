class Solution {
    public int carFleet(int target, int[] position, int[] speed) {
        int n = position.length;
        Integer[] idx = new Integer[n];
        for (int i = 0; i < n; i++) idx[i] = i;
        Arrays.sort(idx, (a, b) -> Integer.compare(position[b], position[a]));
        Deque<long[]> stack = new ArrayDeque<>();
        for (int i : idx) {
            long dist = (long) target - position[i];
            long spd = speed[i];
            if (stack.isEmpty() || dist * stack.peek()[1] > stack.peek()[0] * spd) {
                stack.push(new long[]{dist, spd});
            }
        }
        return stack.size();
    }
}
