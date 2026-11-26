class Solution {
    public int getMaximumConsecutive(int[] coins) {
        int[] a = coins.clone(); Arrays.sort(a); int reach = 0;
        for (int coin : a) { if (coin > reach + 1) break; reach += coin; }
        return reach;
    }
}
