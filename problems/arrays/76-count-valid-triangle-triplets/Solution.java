class Solution {
    public long triangleNumber(int[] nums) {
        int[] a = nums.clone(); Arrays.sort(a); long count = 0;
        for (int k = a.length - 1; k >= 2; k--) { int i = 0, j = k - 1; while (i < j) { if ((long)a[i] + a[j] > a[k]) { count += j - i; j--; } else i++; } }
        return count;
    }
}
