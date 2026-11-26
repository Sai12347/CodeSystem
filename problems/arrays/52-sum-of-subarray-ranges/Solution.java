class Solution {
    public long sumSubarrayRanges(int[] nums) {
        long maximum = 0, minimum = 0; int n = nums.length; int[] stack = new int[n + 1];
        for (int pass = 0; pass < 2; pass++) { int size = 0; boolean isMin = pass == 1;
            for (int i = 0; i <= n; i++) {
                while (size > 0 && (i == n || (isMin ? nums[stack[size - 1]] >= nums[i] : nums[stack[size - 1]] <= nums[i]))) { int mid = stack[--size]; int left = size > 0 ? stack[size - 1] : -1; long v = (long) nums[mid] * (mid - left) * (i - mid); if (isMin) minimum += v; else maximum += v; }
                stack[size++] = i;
            }
        }
        return maximum - minimum;
    }
}
