class Solution {
    public int[] matchingBracketIndices(String s) {
        int n = s.length();
        int[] ans = new int[n];
        Arrays.fill(ans, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(i);
            } else if (ch == ')' || ch == ']' || ch == '}') {
                int j = stack.pop();
                ans[i] = j;
                ans[j] = i;
            }
        }
        return ans;
    }
}
