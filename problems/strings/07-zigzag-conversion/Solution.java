class Solution {
    public String convert(String s, int numRows) {
        int n = s.length();
        if (numRows == 1 || numRows >= n) {
            return s;
        }
        int cycle = 2 * (numRows - 1);
        StringBuilder out = new StringBuilder(n);
        for (int r = 0; r < numRows; r++) {
            for (int i = r; i < n; i += cycle) {
                out.append(s.charAt(i));
                if (r > 0 && r < numRows - 1) {
                    int diag = i + cycle - 2 * r;
                    if (diag < n) {
                        out.append(s.charAt(diag));
                    }
                }
            }
        }
        return out.toString();
    }
}
