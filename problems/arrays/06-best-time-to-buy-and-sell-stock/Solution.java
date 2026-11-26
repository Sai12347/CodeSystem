class Solution {
    public int maxProfit(int[] prices) {
        int minPrice = prices[0];
        int best = 0;
        for (int i = 1; i < prices.length; i++) {
            if (prices[i] < minPrice) {
                minPrice = prices[i];
            } else if (prices[i] - minPrice > best) {
                best = prices[i] - minPrice;
            }
        }
        return best;
    }
}
