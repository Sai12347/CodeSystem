class Solution {
    public List<Integer> pancakeSort(int[] arr) {
        List<Integer> res = new ArrayList<>();
        int n = arr.length;
        for (int val = n; val >= 2; val--) {
            int idx = 0;
            while (arr[idx] != val) {
                idx++;
            }
            if (idx == val - 1) {
                continue;
            }
            if (idx > 0) {
                reverse(arr, idx + 1);
                res.add(idx + 1);
            }
            reverse(arr, val);
            res.add(val);
        }
        return res;
    }

    private void reverse(int[] a, int k) {
        for (int l = 0, r = k - 1; l < r; l++, r--) {
            int tmp = a[l];
            a[l] = a[r];
            a[r] = tmp;
        }
    }
}
