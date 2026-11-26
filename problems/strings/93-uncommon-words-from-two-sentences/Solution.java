class Solution {
    public String[] uncommonFromSentences(String s1, String s2) {
        Map<String, Integer> cnt = new HashMap<>();
        for (String w : s1.split(" ")) cnt.put(w, cnt.getOrDefault(w, 0) + 1);
        for (String w : s2.split(" ")) cnt.put(w, cnt.getOrDefault(w, 0) + 1);
        List<String> out = new ArrayList<>();
        for (Map.Entry<String, Integer> e : cnt.entrySet()) {
            if (e.getValue() == 1) out.add(e.getKey());
        }
        return out.toArray(new String[0]);
    }
}
