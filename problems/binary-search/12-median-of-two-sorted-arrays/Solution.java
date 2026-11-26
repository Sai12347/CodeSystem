class Solution {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int[] A = nums1;
        int[] B = nums2;
        if (A.length > B.length) {
            int[] tmp = A;
            A = B;
            B = tmp;
        }
        int m = A.length;
        int n = B.length;
        int half = (m + n + 1) / 2;
        int lo = 0;
        int hi = m;

        while (lo <= hi) {
            int i = lo + (hi - lo) / 2;
            int j = half - i;

            int aLeft = (i > 0) ? A[i - 1] : Integer.MIN_VALUE;
            int aRight = (i < m) ? A[i] : Integer.MAX_VALUE;
            int bLeft = (j > 0) ? B[j - 1] : Integer.MIN_VALUE;
            int bRight = (j < n) ? B[j] : Integer.MAX_VALUE;

            if (aLeft <= bRight && bLeft <= aRight) {
                if ((m + n) % 2 == 1) {
                    return (double) Math.max(aLeft, bLeft);
                }
                return ((long) Math.max(aLeft, bLeft) + Math.min(aRight, bRight)) / 2.0;
            } else if (aLeft > bRight) {
                hi = i - 1;
            } else {
                lo = i + 1;
            }
        }
        return 0.0;
    }
}
