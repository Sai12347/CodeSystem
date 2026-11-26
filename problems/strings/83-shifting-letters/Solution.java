class Solution {
    public String shiftingLetters(String s, int[] shifts) {
        int n = s.length();
        char[] chars = s.toCharArray();
        int acc = 0;
        for (int i = n - 1; i >= 0; i--) {
            acc = (acc + shifts[i] % 26) % 26;
            chars[i] = (char) ('a' + (chars[i] - 'a' + acc) % 26);
        }
        return new String(chars);
    }
}
