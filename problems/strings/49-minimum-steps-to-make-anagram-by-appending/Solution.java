class Solution {
    public int minStepsToAnagram(String s, String t) {
        int[] diff = new int[26];
        for (int i = 0; i < s.length(); i++) diff[s.charAt(i) - 'a']++;
        for (int i = 0; i < t.length(); i++) diff[t.charAt(i) - 'a']--;
        int steps = 0;
        for (int v : diff) steps += Math.abs(v);
        return steps;
    }
}
