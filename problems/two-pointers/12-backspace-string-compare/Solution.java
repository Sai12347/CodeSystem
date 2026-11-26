class Solution {
    public boolean backspaceCompare(String s, String t) {
        int i = s.length() - 1;
        int j = t.length() - 1;
        while (i >= 0 || j >= 0) {
            i = nextValid(s, i);
            j = nextValid(t, j);
            if (i < 0 && j < 0) {
                return true;
            }
            if (i < 0 || j < 0 || s.charAt(i) != t.charAt(j)) {
                return false;
            }
            i--;
            j--;
        }
        return true;
    }

    private int nextValid(String text, int idx) {
        int skip = 0;
        while (idx >= 0) {
            if (text.charAt(idx) == '#') {
                skip++;
            } else if (skip > 0) {
                skip--;
            } else {
                return idx;
            }
            idx--;
        }
        return -1;
    }
}
