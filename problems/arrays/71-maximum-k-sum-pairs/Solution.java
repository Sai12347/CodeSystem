class Solution {
    public int maxKSumPairs(int[] nums, int k) {
        int[] a = nums.clone(); Arrays.sort(a); int i = 0, j = a.length - 1, pairs = 0;
        while (i < j) { long sum = (long)a[i] + a[j]; if (sum == k) { pairs++; i++; j--; } else if (sum < k) i++; else j--; }
        return pairs;
    }
}
