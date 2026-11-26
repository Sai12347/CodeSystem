class Solution {
    public void wiggleSort(int[] nums) {
        int n = nums.length;
        if (n <= 1) {
            return;
        }
        int median = findKth(nums, n / 2);
        int m = n | 1;
        int left = 0, i = 0, right = n - 1;
        while (i <= right) {
            int vi = (1 + 2 * i) % m;
            if (nums[vi] > median) {
                int vl = (1 + 2 * left) % m;
                swap(nums, vl, vi);
                left++;
                i++;
            } else if (nums[vi] < median) {
                int vr = (1 + 2 * right) % m;
                swap(nums, vi, vr);
                right--;
            } else {
                i++;
            }
        }
    }

    private int findKth(int[] nums, int k) {
        int lo = 0, hi = nums.length - 1;
        Random rng = new Random(42);
        while (lo <= hi) {
            int pivot = nums[lo + rng.nextInt(hi - lo + 1)];
            int lt = lo, i = lo, gt = hi;
            while (i <= gt) {
                if (nums[i] < pivot) {
                    swap(nums, lt++, i++);
                } else if (nums[i] > pivot) {
                    swap(nums, i, gt--);
                } else {
                    i++;
                }
            }
            if (k < lt) {
                hi = lt - 1;
            } else if (k > gt) {
                lo = gt + 1;
            } else {
                return pivot;
            }
        }
        return nums[k];
    }

    private void swap(int[] a, int i, int j) {
        int tmp = a[i];
        a[i] = a[j];
        a[j] = tmp;
    }
}
