class Solution {
    public String findLongestWord(String s, String[] dictionary) {
        String best = "";
        int n = s.length();
        for (String w : dictionary) {
            if (w.length() < best.length() || (w.length() == best.length() && w.compareTo(best) >= 0)) {
                continue;
            }
            int i = 0, j = 0, m = w.length();
            while (i < n && j < m) {
                if (s.charAt(i) == w.charAt(j)) j++;
                i++;
            }
            if (j == m) best = w;
        }
        return best;
    }
}
