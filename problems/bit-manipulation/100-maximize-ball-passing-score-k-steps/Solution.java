class Solution {
    public long maxBallPassingScore(int[] receiver, long k) {
        int n = receiver.length;
        int[] up = receiver.clone();
        long[] w = new long[n];
        int[] pos = new int[n];
        long[] score = new long[n];
        for (int i = 0; i < n; i++) {
            w[i] = receiver[i];
            pos[i] = i;
            score[i] = i;
        }
        long rem = k;
        while (rem > 0L) {
            if ((rem & 1L) != 0L) {
                for (int i = 0; i < n; i++) {
                    int p = pos[i];
                    score[i] += w[p];
                    pos[i] = up[p];
                }
            }
            rem >>= 1;
            if (rem > 0L) {
                int[] newUp = new int[n];
                long[] newW = new long[n];
                for (int i = 0; i < n; i++) {
                    int mid = up[i];
                    newUp[i] = up[mid];
                    newW[i] = w[i] + w[mid];
                }
                up = newUp;
                w = newW;
            }
        }
        long best = score[0];
        for (int i = 1; i < n; i++) {
            if (score[i] > best) best = score[i];
        }
        return best;
    }
}
