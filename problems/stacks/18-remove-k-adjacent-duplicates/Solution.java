class Solution {
    public String removeDuplicates(String s, int k) {
        int n = s.length();
        char[] chars = new char[n];
        int[] counts = new int[n];
        int top = 0;
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (top > 0 && chars[top - 1] == ch) {
                if (++counts[top - 1] == k) {
                    top--;
                }
            } else {
                chars[top] = ch;
                counts[top] = 1;
                top++;
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < top; i++) {
            for (int c = 0; c < counts[i]; c++) {
                sb.append(chars[i]);
            }
        }
        return sb.toString();
    }
}
