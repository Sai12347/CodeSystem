class Solution {
    public int countPalindromicSubsequence(String s) {
        int[] first = new int[26];
        int[] last = new int[26];
        Arrays.fill(first, -1);
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            if (first[idx] == -1) first[idx] = i;
            last[idx] = i;
        }
        int ans = 0;
        for (int c = 0; c < 26; c++) {
            if (first[c] != -1 && first[c] + 1 < last[c]) {
                int seen = 0;
                for (int i = first[c] + 1; i < last[c]; i++) {
                    seen |= 1 << (s.charAt(i) - 'a');
                }
                ans += Integer.bitCount(seen);
            }
        }
        return ans;
    }
}
