class Solution {
    public boolean checkInclusion(String s1, String s2) {
        int m = s1.length();
        int n = s2.length();
        if (m > n) {
            return false;
        }

        int[] need = new int[26];
        int[] win = new int[26];
        for (int i = 0; i < m; i++) {
            need[s1.charAt(i) - 'a']++;
            win[s2.charAt(i) - 'a']++;
        }

        int matches = 0;
        for (int c = 0; c < 26; c++) {
            if (need[c] == win[c]) {
                matches++;
            }
        }
        if (matches == 26) {
            return true;
        }

        for (int right = m; right < n; right++) {
            int addIdx = s2.charAt(right) - 'a';
            if (win[addIdx] == need[addIdx]) {
                matches--;
            }
            win[addIdx]++;
            if (win[addIdx] == need[addIdx]) {
                matches++;
            }

            int remIdx = s2.charAt(right - m) - 'a';
            if (win[remIdx] == need[remIdx]) {
                matches--;
            }
            win[remIdx]--;
            if (win[remIdx] == need[remIdx]) {
                matches++;
            }

            if (matches == 26) {
                return true;
            }
        }

        return false;
    }
}
