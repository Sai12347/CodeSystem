class Solution {
    public int numMatchingSubseq(String s, String[] words) {
        @SuppressWarnings("unchecked")
        List<int[]>[] buckets = new ArrayList[26];
        for (int i = 0; i < 26; i++) buckets[i] = new ArrayList<>();
        for (int i = 0; i < words.length; i++) {
            buckets[words[i].charAt(0) - 'a'].add(new int[]{i, 0});
        }
        int ans = 0;
        for (int i = 0; i < s.length(); i++) {
            int idx = s.charAt(i) - 'a';
            List<int[]> cur = buckets[idx];
            buckets[idx] = new ArrayList<>();
            for (int[] pair : cur) {
                int wi = pair[0], pos = pair[1] + 1;
                if (pos == words[wi].length()) ans++;
                else buckets[words[wi].charAt(pos) - 'a'].add(new int[]{wi, pos});
            }
        }
        return ans;
    }
}
