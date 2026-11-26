class Solution {
    public int minimumAverageDifference(int[] nums) {
        long total = 0, left = 0; for (int x : nums) total += x;
        long best = Long.MAX_VALUE; int answer = 0;
        for (int i = 0; i < nums.length; i++) { left += nums[i]; long a = left / (i + 1); long b = i + 1 < nums.length ? (total-left)/(nums.length-i-1) : 0; long d = Math.abs(a-b); if (d < best) { best=d; answer=i; } }
        return answer;
    }
}
