class Solution {
    public int[] sortBySetBits(int[] arr) {
        int n = arr.length;
        int[] packed = new int[n];
        for (int i = 0; i < n; i++) {
            packed[i] = (Integer.bitCount(arr[i]) << 20) | arr[i];
        }
        Arrays.sort(packed);
        for (int i = 0; i < n; i++) {
            packed[i] &= 0xFFFFF;
        }
        return packed;
    }
}
