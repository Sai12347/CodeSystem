class Solution {
    public int maxChunksToSorted(int[] nums) {
        int chunks = 0, high = 0;
        for (int i = 0; i < nums.length; i++) { high = Math.max(high, nums[i]); if (high == i) chunks++; }
        return chunks;
    }
}
