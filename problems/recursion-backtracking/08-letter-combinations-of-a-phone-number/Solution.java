class Solution {
    private static final String[] KEYPAD = {
        "", "", "abc", "def", "ghi", "jkl", "mno", "pqrs", "tuv", "wxyz"
    };

    public List<String> letterCombinations(String digits) {
        List<String> res = new ArrayList<>();
        if (digits == null || digits.isEmpty()) {
            return res;
        }
        StringBuilder path = new StringBuilder();
        dfs(digits, 0, path, res);
        return res;
    }

    private void dfs(String digits, int idx, StringBuilder path, List<String> res) {
        if (idx == digits.length()) {
            res.add(path.toString());
            return;
        }
        String letters = KEYPAD[digits.charAt(idx) - '0'];
        for (int i = 0; i < letters.length(); i++) {
            path.append(letters.charAt(i));
            dfs(digits, idx + 1, path, res);
            path.deleteCharAt(path.length() - 1);
        }
    }
}
