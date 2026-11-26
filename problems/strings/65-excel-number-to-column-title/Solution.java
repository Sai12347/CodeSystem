class Solution {
    public String convertToTitle(int columnNumber) {
        StringBuilder out = new StringBuilder();
        int n = columnNumber;
        while (n > 0) {
            n--;
            out.append((char) ('A' + n % 26));
            n /= 26;
        }
        return out.reverse().toString();
    }
}
