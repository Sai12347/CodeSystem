class Solution {
    public String compressString(String s) {
        StringBuilder out = new StringBuilder();
        int n = s.length(), i = 0;
        while (i < n) {
            int j = i + 1;
            while (j < n && s.charAt(j) == s.charAt(i)) j++;
            out.append(s.charAt(i));
            if (j - i > 1) out.append(j - i);
            i = j;
        }
        return out.toString();
    }
}
