class Solution {
    public boolean validateStackSequences(int[] pushed, int[] popped) {
        int n = pushed.length;
        int[] stack = new int[n];
        int top = -1;
        int j = 0;
        for (int val : pushed) {
            stack[++top] = val;
            while (top >= 0 && j < n && stack[top] == popped[j]) {
                top--;
                j++;
            }
        }
        return j == n;
    }
}
