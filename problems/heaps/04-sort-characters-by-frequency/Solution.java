class Solution {
    public String frequencySort(String s) {
        Map<Character, Integer> counts = new HashMap<>();
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            counts.merge(c, 1, Integer::sum);
        }
        PriorityQueue<Map.Entry<Character, Integer>> maxHeap =
            new PriorityQueue<>((a, b) -> Integer.compare(b.getValue(), a.getValue()));
        maxHeap.addAll(counts.entrySet());
        StringBuilder sb = new StringBuilder(s.length());
        while (!maxHeap.isEmpty()) {
            Map.Entry<Character, Integer> entry = maxHeap.poll();
            char ch = entry.getKey();
            int freq = entry.getValue();
            for (int i = 0; i < freq; i++) {
                sb.append(ch);
            }
        }
        return sb.toString();
    }
}
