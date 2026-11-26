class Solution {
    public int totalFruit(int[] fruits) {
        Map<Integer, Integer> counts = new HashMap<>();
        int left = 0;
        int best = 0;
        for (int right = 0; right < fruits.length; right++) {
            int f = fruits[right];
            counts.put(f, counts.getOrDefault(f, 0) + 1);
            while (counts.size() > 2) {
                int lf = fruits[left];
                int c = counts.get(lf) - 1;
                if (c == 0) {
                    counts.remove(lf);
                } else {
                    counts.put(lf, c);
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
