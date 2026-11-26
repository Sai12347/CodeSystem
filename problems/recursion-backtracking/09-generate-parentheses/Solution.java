class Solution {
    public List<String> generateParenthesis(int n) {
        List<String> res = new ArrayList<>();
        char[] buf = new char[2 * n];
        backtrack(n, 0, 0, buf, res);
        return res;
    }

    private void backtrack(int n, int open, int close, char[] buf, List<String> res) {
        int idx = open + close;
        if (idx == buf.length) {
            res.add(new String(buf));
            return;
        }
        if (open < n) {
            buf[idx] = '(';
            backtrack(n, open + 1, close, buf, res);
        }
        if (close < open) {
            buf[idx] = ')';
            backtrack(n, open, close + 1, buf, res);
        }
    }
}
