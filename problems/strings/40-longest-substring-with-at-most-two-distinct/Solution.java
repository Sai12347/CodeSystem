class Solution {
    public int lengthOfLongestSubstringTwoDistinct(String s) {
        Map<Character, Integer> counts = new HashMap<>(); int left = 0, best = 0;
        for (int right = 0; right < s.length(); right++) { char c = s.charAt(right); counts.put(c, counts.getOrDefault(c, 0) + 1); while (counts.size() > 2) { char x = s.charAt(left++); int n = counts.get(x) - 1; if (n == 0) counts.remove(x); else counts.put(x, n); } best = Math.max(best, right - left + 1); }
        return best;
    }
}
