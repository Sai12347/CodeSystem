class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> wList = (List<Object>) inp.get("w");
        int trials = ((Number) inp.get("trials")).intValue();
        int n = wList.size();
        int[] w = new int[n];
        int[] copy = new int[n];
        long total = 0;
        for (int i = 0; i < n; i++) {
            int val = ((Number) wList.get(i)).intValue();
            w[i] = val;
            copy[i] = val;
            total += val;
        }
        Solution sol = new Solution(copy);
        int[] counts = new int[n];
        for (int t = 0; t < trials; t++) {
            int idx = sol.pickIndex();
            if (idx < 0 || idx >= n) {
                return "pickIndex() returned out-of-range index " + idx + " for length " + n;
            }
            counts[idx]++;
        }
        for (int i = 0; i < n; i++) {
            double p = (double) w[i] / total;
            double obs = (double) counts[i] / trials;
            double tol = Math.max(0.035, 6.5 * Math.sqrt(p * (1.0 - p) / trials));
            if (Math.abs(obs - p) > tol) {
                return String.format("Distribution mismatch at index %d: expected %.4f, got %.4f", i, p, obs);
            }
        }
        if (n > 10) {
            int blocks = 4;
            for (int b = 0; b < blocks; b++) {
                int lo = (b * n) / blocks;
                int hi = ((b + 1) * n) / blocks;
                long wSum = 0;
                int cSum = 0;
                for (int i = lo; i < hi; i++) {
                    wSum += w[i];
                    cSum += counts[i];
                }
                double p = (double) wSum / total;
                double obs = (double) cSum / trials;
                double tol = Math.max(0.035, 6.5 * Math.sqrt(p * (1.0 - p) / trials));
                if (Math.abs(obs - p) > tol) {
                    return String.format("Distribution mismatch in block [%d, %d): expected %.4f, got %.4f", lo, hi, p, obs);
                }
            }
        }
        return true;
    }
}
