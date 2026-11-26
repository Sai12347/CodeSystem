class Solution {
    public long countIncreasingSubarrays(int[] nums) {
        long answer = 0; int run = 0;
        for (int i = 0; i < nums.length; i++) { run = i > 0 && nums[i] > nums[i - 1] ? run + 1 : 1; answer += run; }
        return answer;
    }
}
