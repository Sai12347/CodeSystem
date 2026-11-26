class Solution {
    public int minSwapsBalanced(String s) {
        int close = 0, maxClose = 0;
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '[') close--;
            else {
                close++;
                if (close > maxClose) maxClose = close;
            }
        }
        return (maxClose + 1) / 2;
    }
}
