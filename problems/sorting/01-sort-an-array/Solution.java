class Solution {
    public int[] sortArray(int[] nums) {
        int n = nums.length;
        if (n <= 1) {
            return nums;
        }
        int[] buf = new int[n];
        mergeSort(nums, buf, 0, n);
        return nums;
    }

    private void mergeSort(int[] nums, int[] buf, int lo, int hi) {
        if (hi - lo <= 1) {
            return;
        }
        int mid = lo + (hi - lo) / 2;
        mergeSort(nums, buf, lo, mid);
        mergeSort(nums, buf, mid, hi);
        if (nums[mid - 1] <= nums[mid]) {
            return;
        }
        int i = lo, j = mid, k = lo;
        while (i < mid && j < hi) {
            if (nums[i] <= nums[j]) {
                buf[k++] = nums[i++];
            } else {
                buf[k++] = nums[j++];
            }
        }
        while (i < mid) {
            buf[k++] = nums[i++];
        }
        while (j < hi) {
            buf[k++] = nums[j++];
        }
        System.arraycopy(buf, lo, nums, lo, hi - lo);
    }
}
