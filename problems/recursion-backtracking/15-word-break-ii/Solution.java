class Solution {
    public List<String> wordBreak(String s, List<String> wordDict) {
        Set<String> words = new HashSet<>(wordDict);
        int maxLen = 0;
        for (String w : words) {
            maxLen = Math.max(maxLen, w.length());
        }
        Map<Integer, List<String>> memo = new HashMap<>();
        return dfs(s, 0, maxLen, words, memo);
    }

    private List<String> dfs(String s, int start, int maxLen, Set<String> words,
                             Map<Integer, List<String>> memo) {
        if (memo.containsKey(start)) return memo.get(start);
        List<String> res = new ArrayList<>();
        int n = s.length();
        if (start == n) {
            res.add("");
            return res;
        }
        int limit = Math.min(n, start + maxLen);
        for (int end = start + 1; end <= limit; end++) {
            String w = s.substring(start, end);
            if (words.contains(w)) {
                for (String tail : dfs(s, end, maxLen, words, memo)) {
                    res.add(tail.isEmpty() ? w : w + " " + tail);
                }
            }
        }
        memo.put(start, res);
        return res;
    }
}
