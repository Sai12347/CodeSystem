class Solution {
    public int findTheLongestSubstring(String s) {
        int[] first = new int[32];
        Arrays.fill(first, -2);
        first[0] = -1;
        int mask = 0;
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            switch (s.charAt(i)) {
                case 'a' -> mask ^= 1;
                case 'e' -> mask ^= 2;
                case 'i' -> mask ^= 4;
                case 'o' -> mask ^= 8;
                case 'u' -> mask ^= 16;
                default -> {}
            }
            if (first[mask] != -2) {
                int len = i - first[mask];
                if (len > best) {
                    best = len;
                }
            } else {
                first[mask] = i;
            }
        }
        return best;
    }
}
