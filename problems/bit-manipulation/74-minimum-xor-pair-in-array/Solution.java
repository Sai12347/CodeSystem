class Solution {
    public int minXorPair(int[] nums) {
        int[] arr = nums.clone();
        Arrays.sort(arr);
        int ans = arr[0] ^ arr[1];
        for (int i = 1; i < arr.length - 1; i++) {
            int v = arr[i] ^ arr[i + 1];
            if (v < ans) ans = v;
        }
        return ans;
    }
}
