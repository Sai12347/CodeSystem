class Solution {
    public long maximumHappiness(int[] happiness, int k) {
        int[] a = happiness.clone(); Arrays.sort(a); long total = 0;
        for (int i = 0; i < k; i++) total += Math.max(0L, (long)a[a.length-1-i] - i);
        return total;
    }
}
