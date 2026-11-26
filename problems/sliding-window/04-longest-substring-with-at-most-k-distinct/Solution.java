class Solution {
    public int lengthOfLongestSubstringKDistinct(String s, int k) {
        if (k == 0) {
            return 0;
        }
        Map<Character, Integer> counts = new HashMap<>();
        int left = 0;
        int best = 0;
        for (int right = 0; right < s.length(); right++) {
            char ch = s.charAt(right);
            counts.put(ch, counts.getOrDefault(ch, 0) + 1);
            while (counts.size() > k) {
                char leftCh = s.charAt(left);
                int c = counts.get(leftCh) - 1;
                if (c == 0) {
                    counts.remove(leftCh);
                } else {
                    counts.put(leftCh, c);
                }
                left++;
            }
            int len = right - left + 1;
            if (len > best) {
                best = len;
            }
        }
        return best;
    }
}
