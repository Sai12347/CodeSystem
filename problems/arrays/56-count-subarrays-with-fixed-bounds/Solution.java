class Solution {
    public long countSubarraysWithFixedBounds(int[] nums, int minK, int maxK) {
        long answer = 0; int lastBad = -1, lastMin = -1, lastMax = -1;
        for (int i = 0; i < nums.length; i++) { int x = nums[i]; if (x < minK || x > maxK) lastBad = i; if (x == minK) lastMin = i; if (x == maxK) lastMax = i; answer += Math.max(0, Math.min(lastMin, lastMax) - lastBad); }
        return answer;
    }
}
