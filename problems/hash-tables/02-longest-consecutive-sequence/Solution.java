class Solution {
    public int longestConsecutive(int[] nums) {
        Set<Integer> set = new HashSet<>(nums.length * 2);
        for (int num : nums) {
            set.add(num);
        }
        int best = 0;
        for (int x : set) {
            if (!set.contains(x - 1)) {
                int curr = x;
                while (set.contains(curr + 1)) {
                    curr++;
                }
                best = Math.max(best, curr - x + 1);
            }
        }
        return best;
    }
}
