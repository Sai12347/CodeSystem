class Solution {
    public int[] grayCode(int n) {
        int size = 1 << n;
        int[] ans = new int[size];
        for (int i = 0; i < size; i++) {
            ans[i] = i ^ (i >> 1);
        }
        return ans;
    }
}
