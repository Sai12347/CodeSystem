class Solution {
    public String reorganizeString(String s) {
        int n = s.length();
        int[] freq = new int[26];
        int maxFreq = 0;
        for (int i = 0; i < n; i++) {
            int f = ++freq[s.charAt(i) - 'a'];
            if (f > maxFreq) maxFreq = f;
        }
        if (maxFreq > (n + 1) / 2) {
            return "";
        }
        PriorityQueue<int[]> maxHeap = new PriorityQueue<>((a, b) -> Integer.compare(b[0], a[0]));
        for (int i = 0; i < 26; i++) {
            if (freq[i] > 0) {
                maxHeap.offer(new int[]{freq[i], i});
            }
        }
        StringBuilder sb = new StringBuilder(n);
        int[] prev = null;
        while (!maxHeap.isEmpty()) {
            int[] cur = maxHeap.poll();
            sb.append((char) ('a' + cur[1]));
            cur[0]--;
            if (prev != null && prev[0] > 0) {
                maxHeap.offer(prev);
            }
            prev = cur;
        }
        return sb.toString();
    }
}
