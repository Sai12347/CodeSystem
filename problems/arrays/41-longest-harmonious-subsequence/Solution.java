class Solution {
    public int longestHarmoniousSubsequence(int[] nums) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);
        int best = 0;
        for (Map.Entry<Integer, Integer> entry : counts.entrySet()) {
            Integer next = counts.get(entry.getKey() + 1);
            if (next != null) best = Math.max(best, entry.getValue() + next);
        }
        return best;
    }
}
