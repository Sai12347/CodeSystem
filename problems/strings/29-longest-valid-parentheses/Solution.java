class Solution {
    public int longestValidParentheses(String s) {
        int[] stack = new int[s.length() + 1]; int size = 1; stack[0] = -1; int best = 0;
        for (int i = 0; i < s.length(); i++) { if (s.charAt(i) == '(') stack[size++] = i; else { size--; if (size == 0) stack[size++] = i; else best = Math.max(best, i - stack[size - 1]); } }
        return best;
    }
}
