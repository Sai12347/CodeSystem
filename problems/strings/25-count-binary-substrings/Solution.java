class Solution {
    public int countBinarySubstrings(String s) {
        int previous = 0, run = 1, total = 0;
        for (int i = 1; i < s.length(); i++) { if (s.charAt(i) == s.charAt(i - 1)) run++; else { total += Math.min(previous, run); previous = run; run = 1; } }
        return total + Math.min(previous, run);
    }
}
