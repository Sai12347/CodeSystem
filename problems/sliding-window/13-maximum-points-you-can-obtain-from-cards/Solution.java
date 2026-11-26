class Solution {
    public int maxScore(int[] cardPoints, int k) {
        int n = cardPoints.length;
        int cur = 0;
        for (int i = 0; i < k; i++) {
            cur += cardPoints[i];
        }
        int best = cur;
        for (int i = 1; i <= k; i++) {
            cur += cardPoints[n - i] - cardPoints[k - i];
            if (cur > best) {
                best = cur;
            }
        }
        return best;
    }
}
