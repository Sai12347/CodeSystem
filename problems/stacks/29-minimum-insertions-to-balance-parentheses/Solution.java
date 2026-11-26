class Solution {
    public int minInsertions(String s) {
        int insertions = 0;
        int opens = 0;
        int n = s.length();
        for (int i = 0; i < n; ) {
            if (s.charAt(i) == '(') {
                opens++;
                i++;
            } else {
                if (i + 1 < n && s.charAt(i + 1) == ')') {
                    i += 2;
                } else {
                    insertions++;
                    i++;
                }
                if (opens > 0) {
                    opens--;
                } else {
                    insertions++;
                }
            }
        }
        return insertions + 2 * opens;
    }
}
