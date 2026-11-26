class Solution {
    public String smallestGoodBase(String n) {
        long val = Long.parseLong(n);
        int maxM = 63 - Long.numberOfLeadingZeros(val);
        for (int m = maxM; m >= 2; m--) {
            long lo = 2, hi = val - 1;
            while (lo <= hi) {
                long mid = lo + ((hi - lo) >>> 1);
                long total = 1;
                long term = 1;
                boolean over = false;
                for (int i = 0; i < m; i++) {
                    if (term > (val - total) / mid) {
                        over = true;
                        break;
                    }
                    term *= mid;
                    total += term;
                }
                if (!over && total == val) {
                    return Long.toString(mid);
                }
                if (over) {
                    hi = mid - 1;
                } else {
                    lo = mid + 1;
                }
            }
        }
        return Long.toString(val - 1);
    }
}
