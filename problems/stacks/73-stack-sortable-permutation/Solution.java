class Solution {
    public boolean canSortWithStack(int[] perm) {
        Deque<Integer> stack = new ArrayDeque<>();
        int need = 1;
        for (int x : perm) {
            stack.push(x);
            while (!stack.isEmpty() && stack.peek() == need) {
                stack.pop();
                need++;
            }
        }
        return need == perm.length + 1;
    }
}
