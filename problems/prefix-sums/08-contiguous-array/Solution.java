class Solution {
    public int findMaxLength(int[] nums) {
        Map<Integer, Integer> firstSeen = new HashMap<>();
        firstSeen.put(0, -1);
        int balance = 0;
        int best = 0;
        for (int i = 0; i < nums.length; i++) {
            balance += (nums[i] == 1) ? 1 : -1;
            Integer prev = firstSeen.get(balance);
            if (prev != null) {
                int len = i - prev;
                if (len > best) {
                    best = len;
                }
            } else {
                firstSeen.put(balance, i);
            }
        }
        return best;
    }
}
