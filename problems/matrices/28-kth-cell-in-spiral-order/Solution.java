class Solution {
    public int[] kthSpiralCell(int rows, int cols, long k) {
        long R = rows, C = cols;
        long total = R * C;
        long lo = 0, hi = (Math.min(R, C) - 1) / 2;
        while (lo < hi) {
            long mid = (lo + hi + 1) / 2;
            long consumed = total - (R - 2 * mid) * (C - 2 * mid);
            if (consumed < k) lo = mid;
            else hi = mid - 1;
        }
        long layer = lo;
        long consumed = total - (R - 2 * layer) * (C - 2 * layer);
        long rem = k - 1 - consumed;
        long top = layer, bottom = R - 1 - layer;
        long left = layer, right = C - 1 - layer;
        long w = right - left + 1;
        long h = bottom - top + 1;
        if (rem < w) return new int[]{(int) top, (int) (left + rem)};
        rem -= w;
        if (rem < h - 1) return new int[]{(int) (top + 1 + rem), (int) right};
        rem -= (h - 1);
        if (rem < w - 1) return new int[]{(int) bottom, (int) (right - 1 - rem)};
        rem -= (w - 1);
        return new int[]{(int) (bottom - 1 - rem), (int) left};
    }
}
