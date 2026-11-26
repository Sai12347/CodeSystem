class Solution {
    public int minSteps(String s, String t) {
        int[] diff = new int[26];
        for (int i = 0; i < s.length(); i++) {
            diff[s.charAt(i) - 'a']++;
            diff[t.charAt(i) - 'a']--;
        }
        int steps = 0;
        for (int v : diff) if (v > 0) steps += v;
        return steps;
    }
}
