class Solution {
    public int minArea(char[][] image, int x, int y) {
        int m = image.length, n = image[0].length;
        int lo = 0, hi = x;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (rowHasOne(image, mid)) hi = mid;
            else lo = mid + 1;
        }
        int top = lo;

        lo = x; hi = m - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >>> 1;
            if (rowHasOne(image, mid)) lo = mid;
            else hi = mid - 1;
        }
        int bottom = lo;

        lo = 0; hi = y;
        while (lo < hi) {
            int mid = (lo + hi) >>> 1;
            if (colHasOne(image, mid)) hi = mid;
            else lo = mid + 1;
        }
        int left = lo;

        lo = y; hi = n - 1;
        while (lo < hi) {
            int mid = (lo + hi + 1) >>> 1;
            if (colHasOne(image, mid)) lo = mid;
            else hi = mid - 1;
        }
        int right = lo;

        return (bottom - top + 1) * (right - left + 1);
    }

    private boolean rowHasOne(char[][] image, int r) {
        for (char ch : image[r]) if (ch == '1') return true;
        return false;
    }

    private boolean colHasOne(char[][] image, int c) {
        for (int r = 0; r < image.length; r++) if (image[r][c] == '1') return true;
        return false;
    }
}
