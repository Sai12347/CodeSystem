class Solution {
    public boolean isIsomorphic(String s, String t) {
        int[] lastS = new int[256];
        int[] lastT = new int[256];
        for (int i = 0; i < s.length(); i++) {
            int cs = s.charAt(i);
            int ct = t.charAt(i);
            if (lastS[cs] != lastT[ct]) {
                return false;
            }
            lastS[cs] = i + 1;
            lastT[ct] = i + 1;
        }
        return true;
    }
}
