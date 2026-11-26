class Solution {
    public int maxLengthBetweenEqualCharacters(String s) {
        int[] first = new int[26];
        Arrays.fill(first, -1);
        int best = -1;
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            if (first[idx] == -1) first[idx] = i;
            else best = Math.max(best, i - first[idx] - 1);
        }
        return best;
    }
}
