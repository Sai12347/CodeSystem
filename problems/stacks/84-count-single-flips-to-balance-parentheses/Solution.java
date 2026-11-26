class Solution {
    public int countSingleFlips(String s) {
        int n = s.length();
        int[] pref = new int[n];
        int cur = 0;
        for (int i = 0; i < n; i++) {
            cur += (s.charAt(i) == '(') ? 1 : -1;
            pref[i] = cur;
        }
        if (cur != 2 && cur != -2) return 0;
        int[] sufMin = new int[n];
        sufMin[n - 1] = pref[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            sufMin[i] = Math.min(pref[i], sufMin[i + 1]);
        }
        char target = (cur == 2) ? '(' : ')';
        int needSuf = (cur == 2) ? 2 : -2;
        int ans = 0;
        int prefMin = 0;
        for (int i = 0; i < n; i++) {
            if (prefMin >= 0 && s.charAt(i) == target && sufMin[i] >= needSuf) {
                ans++;
            }
            if (pref[i] < prefMin) prefMin = pref[i];
        }
        return ans;
    }
}
