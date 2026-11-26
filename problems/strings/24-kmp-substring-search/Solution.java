class Solution {
    public int strStr(String haystack, String needle) {
        if (needle.isEmpty()) return 0;
        int[] lps = new int[needle.length()]; int j = 0;
        for (int i = 1; i < needle.length(); i++) { while (j > 0 && needle.charAt(i) != needle.charAt(j)) j = lps[j - 1]; if (needle.charAt(i) == needle.charAt(j)) lps[i] = ++j; }
        j = 0;
        for (int i = 0; i < haystack.length(); i++) {
            while (j > 0 && haystack.charAt(i) != needle.charAt(j)) j = lps[j - 1];
            if (haystack.charAt(i) == needle.charAt(j)) j++;
            if (j == needle.length()) return i - j + 1;
        }
        return -1;
    }
}
