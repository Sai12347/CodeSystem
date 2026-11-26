class Solution {
    public boolean checkAlmostEquivalent(String word1, String word2) {
        int[] counts = new int[26];
        for (int i = 0; i < word1.length(); i++) counts[word1.charAt(i)-'a']++;
        for (int i = 0; i < word2.length(); i++) counts[word2.charAt(i)-'a']--;
        for (int x : counts) if (Math.abs(x) > 3) return false;
        return true;
    }
}
