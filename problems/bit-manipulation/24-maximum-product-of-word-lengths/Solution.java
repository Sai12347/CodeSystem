class Solution {
    public int maxWordLengthProduct(String[] words) {
        Map<Integer, Integer> bestLen = new HashMap<>();
        for (String w : words) {
            int mask = 0;
            for (int i = 0; i < w.length(); i++) {
                mask |= 1 << (w.charAt(i) - 'a');
            }
            bestLen.merge(mask, w.length(), Math::max);
        }
        int m = bestLen.size();
        int[] masks = new int[m];
        int[] lens = new int[m];
        int idx = 0;
        for (Map.Entry<Integer, Integer> e : bestLen.entrySet()) {
            masks[idx] = e.getKey();
            lens[idx] = e.getValue();
            idx++;
        }
        int ans = 0;
        for (int i = 0; i < m; i++) {
            for (int j = i + 1; j < m; j++) {
                if ((masks[i] & masks[j]) == 0) {
                    int prod = lens[i] * lens[j];
                    if (prod > ans) ans = prod;
                }
            }
        }
        return ans;
    }
}
