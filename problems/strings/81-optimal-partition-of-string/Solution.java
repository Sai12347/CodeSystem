class Solution {
    public int partitionString(String s) {
        int parts = 1, mask = 0;
        for (int i = 0; i < s.length(); i++) {
            int bit = 1 << (s.charAt(i) - 'a');
            if ((mask & bit) != 0) {
                parts++;
                mask = bit;
            } else {
                mask |= bit;
            }
        }
        return parts;
    }
}
