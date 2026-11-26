class Solution {
    public int maxChunksToSortedWithDuplicates(int[] arr) {
        int n = arr.length; int[] suffix = new int[n]; suffix[n-1] = arr[n-1];
        for (int i = n - 2; i >= 0; i--) suffix[i] = Math.min(arr[i], suffix[i+1]);
        int chunks = 1, high = arr[0];
        for (int i = 0; i < n - 1; i++) { high = Math.max(high, arr[i]); if (high <= suffix[i+1]) chunks++; }
        return chunks;
    }
}
