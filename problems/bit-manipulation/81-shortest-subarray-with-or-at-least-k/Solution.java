class Solution {
    public int minimumSubarrayLength(int[] nums, int k) {
        int n = nums.length;
        int[] counts = new int[30];
        int curOr = 0;
        int ans = n + 1;
        int left = 0;
        for (int right = 0; right < n; right++) {
            int x = nums[right];
            curOr |= x;
            for (int v = x; v != 0; v &= v - 1) {
                counts[Integer.numberOfTrailingZeros(v)]++;
            }
            while (left <= right && curOr >= k) {
                int len = right - left + 1;
                if (len < ans) ans = len;
                int y = nums[left++];
                for (int v = y; v != 0; v &= v - 1) {
                    int b = Integer.numberOfTrailingZeros(v);
                    if (--counts[b] == 0) {
                        curOr ^= (1 << b);
                    }
                }
            }
        }
        return ans > n ? -1 : ans;
    }
}
