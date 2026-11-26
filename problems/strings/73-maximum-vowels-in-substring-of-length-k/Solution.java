class Solution {
    public int maxVowels(String s, int k) {
        int cur = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            if (isVowel(s.charAt(i))) cur++;
            if (i >= k && isVowel(s.charAt(i - k))) cur--;
            if (i >= k - 1 && cur > best) best = cur;
        }
        return best;
    }
    private boolean isVowel(char c) {
        return c == 'a' || c == 'e' || c == 'i' || c == 'o' || c == 'u';
    }
}
