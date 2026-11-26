class Solution {
    public int[] addNegabinary(int[] arr1, int[] arr2) {
        int i = arr1.length - 1;
        int j = arr2.length - 1;
        int carry = 0;
        List<Integer> list = new ArrayList<>();
        while (i >= 0 || j >= 0 || carry != 0) {
            if (i >= 0) carry += arr1[i--];
            if (j >= 0) carry += arr2[j--];
            list.add(carry & 1);
            carry = -(carry >> 1);
        }
        while (list.size() > 1 && list.get(list.size() - 1) == 0) {
            list.remove(list.size() - 1);
        }
        int n = list.size();
        int[] res = new int[n];
        for (int k = 0; k < n; k++) {
            res[k] = list.get(n - 1 - k);
        }
        return res;
    }
}
