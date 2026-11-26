class Solution {
    public boolean[] camelMatch(String[] queries, String pattern) {
        boolean[] ans = new boolean[queries.length];
        for (int k = 0; k < queries.length; k++) {
            String q = queries[k];
            int j = 0, m = pattern.length();
            boolean valid = true;
            for (int i = 0; i < q.length(); i++) {
                char c = q.charAt(i);
                if (j < m && c == pattern.charAt(j)) j++;
                else if (c >= 'A' && c <= 'Z') { valid = false; break; }
            }
            ans[k] = valid && j == m;
        }
        return ans;
    }
}
