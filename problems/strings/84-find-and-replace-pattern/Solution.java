class Solution {
    public List<String> findAndReplacePattern(String[] words, String pattern) {
        List<String> ans = new ArrayList<>();
        for (String w : words) {
            if (matches(w, pattern)) ans.add(w);
        }
        return ans;
    }
    private boolean matches(String w, String p) {
        int[] p2w = new int[26], w2p = new int[26];
        Arrays.fill(p2w, -1);
        Arrays.fill(w2p, -1);
        for (int i = 0; i < p.length(); i++) {
            int pi = p.charAt(i) - 'a', wi = w.charAt(i) - 'a';
            if (p2w[pi] == -1 && w2p[wi] == -1) {
                p2w[pi] = wi;
                w2p[wi] = pi;
            } else if (p2w[pi] != wi || w2p[wi] != pi) {
                return false;
            }
        }
        return true;
    }
}
