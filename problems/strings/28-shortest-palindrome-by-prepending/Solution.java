class Solution {
    public String shortestPalindrome(String s) {
        String rev = new StringBuilder(s).reverse().toString(); String seq = s + "#" + rev; int[] lps = new int[seq.length()];
        for (int i = 1; i < seq.length(); i++) { int j = lps[i - 1]; while (j > 0 && seq.charAt(i) != seq.charAt(j)) j = lps[j - 1]; if (seq.charAt(i) == seq.charAt(j)) j++; lps[i] = j; }
        int k = lps[seq.length() - 1]; return rev.substring(0, s.length() - k) + s;
    }
}
