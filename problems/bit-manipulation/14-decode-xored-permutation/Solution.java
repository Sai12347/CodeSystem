class Solution {
    public int[] decodeXoredPermutation(int[] encoded) {
        int n = encoded.length + 1;
        int total = 0;
        for (int x = 1; x <= n; x++) {
            total ^= x;
        }
        int oddXor = 0;
        for (int i = 1; i < n - 1; i += 2) {
            oddXor ^= encoded[i];
        }
        int[] perm = new int[n];
        perm[0] = total ^ oddXor;
        for (int i = 0; i < n - 1; i++) {
            perm[i + 1] = perm[i] ^ encoded[i];
        }
        return perm;
    }
}
