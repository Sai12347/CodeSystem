class Solution {
    public int countVowelSubstrings(String word) {
        int[] lastV = {-1, -1, -1, -1, -1};
        int lastC = -1, ans = 0;
        for (int i = 0; i < word.length(); i++) {
            int idx = vowelIndex(word.charAt(i));
            if (idx >= 0) {
                lastV[idx] = i;
                int m = lastV[0];
                for (int k = 1; k < 5; k++) m = Math.min(m, lastV[k]);
                if (m > lastC) ans += m - lastC;
            } else {
                lastC = i;
            }
        }
        return ans;
    }
    private int vowelIndex(char c) {
        switch (c) {
            case 'a': return 0;
            case 'e': return 1;
            case 'i': return 2;
            case 'o': return 3;
            case 'u': return 4;
            default: return -1;
        }
    }
}
