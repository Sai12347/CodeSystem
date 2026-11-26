class Solution {
    public String reverseStr(String s, int k) {
        char[] chars = s.toCharArray();
        for (int start = 0; start < chars.length; start += 2 * k) { int left = start, right = Math.min(start + k, chars.length) - 1; while (left < right) { char c = chars[left]; chars[left++] = chars[right]; chars[right--] = c; } }
        return new String(chars);
    }
}
