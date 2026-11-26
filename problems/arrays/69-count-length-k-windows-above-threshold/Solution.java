class Solution {
    public int numOfWindowsAboveThreshold(int[] nums, int k, int threshold) {
        long target = (long)k * threshold, sum = 0; int answer = 0;
        for (int i = 0; i < k; i++) sum += nums[i]; if (sum >= target) answer++;
        for (int i = k; i < nums.length; i++) { sum += (long)nums[i] - nums[i-k]; if (sum >= target) answer++; }
        return answer;
    }
}
