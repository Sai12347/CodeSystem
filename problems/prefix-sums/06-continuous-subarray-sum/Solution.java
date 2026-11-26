class Solution {
    public boolean checkSubarraySum(int[] nums, int k) {
        Map<Integer, Integer> firstSeen = new HashMap<>();
        firstSeen.put(0, -1);
        long prefix = 0;
        for (int i = 0; i < nums.length; i++) {
            prefix += nums[i];
            int rem = (int) (prefix % k);
            Integer prev = firstSeen.get(rem);
            if (prev != null) {
                if (i - prev >= 2) {
                    return true;
                }
            } else {
                firstSeen.put(rem, i);
            }
        }
        return false;
    }
}
