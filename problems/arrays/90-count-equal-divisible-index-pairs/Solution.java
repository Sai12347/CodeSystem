class Solution {
    public int countEqualDivisiblePairs(int[] nums, int k) {
        int answer = 0;
        for (int i = 0; i < nums.length; i++) for (int j = i + 1; j < nums.length; j++) if (nums[i] == nums[j] && (long)i*j % k == 0) answer++;
        return answer;
    }
}
