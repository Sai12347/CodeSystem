class Solution {
    public long countSubarraysWithMaximum(int[] nums) {
        int maximum = nums[0]; for (int x : nums) maximum = Math.max(maximum, x);
        long answer = 0; int run = 0;
        for (int x : nums) { run = x == maximum ? run + 1 : 0; answer += run; }
        return answer;
    }
}
