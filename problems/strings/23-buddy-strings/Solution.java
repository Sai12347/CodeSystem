class Solution {
    public boolean buddyStrings(String s, String goal) {
        if (s.length() != goal.length()) return false;
        int first = -1, second = -1, mismatches = 0; boolean[] seen = new boolean[26]; boolean duplicate = false;
        for (int i = 0; i < s.length(); i++) { int c = s.charAt(i) - 'a'; if (seen[c]) duplicate = true; seen[c] = true; if (s.charAt(i) != goal.charAt(i)) { if (mismatches == 0) first = i; else if (mismatches == 1) second = i; mismatches++; } }
        if (mismatches == 0) return duplicate;
        return mismatches == 2 && s.charAt(first) == goal.charAt(second) && s.charAt(second) == goal.charAt(first);
    }
}
