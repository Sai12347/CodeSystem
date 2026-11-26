class Solution {
    public boolean checkIfPangram(String sentence) {
        int mask = 0, full = (1 << 26) - 1;
        for (int i = 0; i < sentence.length(); i++) {
            mask |= 1 << (sentence.charAt(i) - 'a');
            if (mask == full) return true;
        }
        return false;
    }
}
