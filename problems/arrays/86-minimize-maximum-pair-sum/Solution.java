class Solution {
    public int minPairSum(int[] nums) {
        int[] a = nums.clone(); Arrays.sort(a); int best = 0;
        for (int i = 0; i < a.length / 2; i++) best = Math.max(best, a[i] + a[a.length-1-i]);
        return best;
    }
}
