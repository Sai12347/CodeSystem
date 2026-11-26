class Solution {
    public int sumOfUnique(int[] nums) {
        Map<Integer, Integer> counts = new HashMap<>();
        for (int x : nums) counts.put(x, counts.getOrDefault(x, 0) + 1);
        int sum = 0; for (Map.Entry<Integer, Integer> e : counts.entrySet()) if (e.getValue() == 1) sum += e.getKey();
        return sum;
    }
}
