class Solution {
    public boolean isAlienSorted(String[] words, String order) {
        int[] rank = new int[26];
        for (int i = 0; i < 26; i++) {
            rank[order.charAt(i) - 'a'] = i;
        }
        for (int i = 0; i < words.length - 1; i++) {
            String w1 = words[i];
            String w2 = words[i + 1];
            int limit = Math.min(w1.length(), w2.length());
            boolean differed = false;
            for (int j = 0; j < limit; j++) {
                int r1 = rank[w1.charAt(j) - 'a'];
                int r2 = rank[w2.charAt(j) - 'a'];
                if (r1 != r2) {
                    if (r1 > r2) {
                        return false;
                    }
                    differed = true;
                    break;
                }
            }
            if (!differed && w1.length() > w2.length()) {
                return false;
            }
        }
        return true;
    }
}
