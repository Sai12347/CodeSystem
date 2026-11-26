class Solution {
    public List<Integer> findAnagrams(String s, String p) {
        List<Integer> res = new ArrayList<>();
        int n = s.length(), m = p.length();
        if (m > n) {
            return res;
        }
        int[] need = new int[26];
        int[] win = new int[26];
        for (int i = 0; i < m; i++) {
            need[p.charAt(i) - 'a']++;
            win[s.charAt(i) - 'a']++;
        }
        int matches = 0;
        for (int i = 0; i < 26; i++) {
            if (need[i] == win[i]) {
                matches++;
            }
        }
        if (matches == 26) {
            res.add(0);
        }
        for (int right = m; right < n; right++) {
            int addIdx = s.charAt(right) - 'a';
            if (win[addIdx] == need[addIdx]) {
                matches--;
            }
            win[addIdx]++;
            if (win[addIdx] == need[addIdx]) {
                matches++;
            }

            int remIdx = s.charAt(right - m) - 'a';
            if (win[remIdx] == need[remIdx]) {
                matches--;
            }
            win[remIdx]--;
            if (win[remIdx] == need[remIdx]) {
                matches++;
            }

            if (matches == 26) {
                res.add(right - m + 1);
            }
        }
        return res;
    }
}
