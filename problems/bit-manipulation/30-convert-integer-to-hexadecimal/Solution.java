class Solution {
    public String toHex(int num) {
        if (num == 0) return "0";
        char[] digits = "0123456789abcdef".toCharArray();
        StringBuilder sb = new StringBuilder();
        int n = num;
        while (n != 0) {
            sb.append(digits[n & 0xF]);
            n >>>= 4;
        }
        return sb.reverse().toString();
    }
}
