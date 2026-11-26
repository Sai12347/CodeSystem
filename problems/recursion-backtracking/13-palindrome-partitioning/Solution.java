class Solution {
    public List<List<String>> partition(String s) {
        int n = s.length();
        boolean[][] isPal = new boolean[n][n];
        for (int i = n - 1; i >= 0; i--) {
            for (int j = i; j < n; j++) {
                if (s.charAt(i) == s.charAt(j) && (j - i <= 2 || isPal[i + 1][j - 1])) {
                    isPal[i][j] = true;
                }
            }
        }

        List<List<String>> res = new ArrayList<>();
        List<String> path = new ArrayList<>();
        backtrack(s, 0, n, isPal, path, res);
        return res;
    }

    private void backtrack(String s, int start, int n, boolean[][] isPal,
                           List<String> path, List<List<String>> res) {
        if (start == n) {
            res.add(new ArrayList<>(path));
            return;
        }
        for (int end = start; end < n; end++) {
            if (isPal[start][end]) {
                path.add(s.substring(start, end + 1));
                backtrack(s, end + 1, n, isPal, path, res);
                path.remove(path.size() - 1);
            }
        }
    }
}
