class Solution {
    public String largestPalindromic(String num) {
        int[] cnt = new int[10];
        for (int i = 0; i < num.length(); i++) cnt[num.charAt(i) - '0']++;
        StringBuilder left = new StringBuilder();
        for (int d = 9; d >= 0; d--) {
            if (d == 0 && left.length() == 0) break;
            int pairs = cnt[d] / 2;
            for (int k = 0; k < pairs; k++) left.append((char) ('0' + d));
            cnt[d] -= pairs * 2;
        }
        String mid = "";
        for (int d = 9; d >= 0; d--) {
            if (cnt[d] > 0) {
                mid = String.valueOf((char) ('0' + d));
                break;
            }
        }
        if (left.length() == 0 && mid.isEmpty()) return "0";
        String l = left.toString();
        return l + mid + left.reverse().toString();
    }
}
