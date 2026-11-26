class Solution {
    public int minimumScoreRange(int[] nums, int k) {
        int[] a = nums.clone(); Arrays.sort(a); int best = Integer.MAX_VALUE;
        for (int i = 0; i + k <= a.length; i++) best = Math.min(best, a[i+k-1]-a[i]);
        return best;
    }
}
