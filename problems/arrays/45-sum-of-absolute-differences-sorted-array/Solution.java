class Solution {
    public long[] getAbsoluteDifferences(int[] nums) {
        int n = nums.length; long total = 0, left = 0;
        for (int x : nums) total += x;
        long[] answer = new long[n];
        for (int i = 0; i < n; i++) { long x = nums[i]; answer[i] = x * i - left + total - left - x * (n - i); left += x; }
        return answer;
    }
}
