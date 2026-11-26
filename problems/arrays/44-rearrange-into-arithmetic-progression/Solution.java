class Solution {
    public boolean canRearrangeArithmeticProgression(int[] nums) {
        int[] a = nums.clone(); Arrays.sort(a);
        long step = (long) a[1] - a[0];
        for (int i = 2; i < a.length; i++) if ((long) a[i] - a[i - 1] != step) return false;
        return true;
    }
}
