class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> raw = (List<Object>) inp.get("arr");
        int n = raw.size();
        int[] orig = new int[n];
        int[] copy = new int[n];
        int[] sim = new int[n];
        for (int i = 0; i < n; i++) {
            int v = ((Number) raw.get(i)).intValue();
            orig[i] = v;
            copy[i] = v;
            sim[i] = v;
        }
        List<Integer> flips = new Solution().pancakeSort(copy);
        if (flips == null) {
            return "Expected non-null List<Integer>, got null";
        }
        if (flips.size() > 10 * n) {
            return "Too many flips: " + flips.size() + " exceeds limit " + (10 * n);
        }
        for (int idx = 0; idx < flips.size(); idx++) {
            Integer kObj = flips.get(idx);
            if (kObj == null) {
                return "Flip #" + idx + " is null";
            }
            int k = kObj;
            if (k < 1 || k > n) {
                return "Flip #" + idx + " value " + k + " out of range [1, " + n + "]";
            }
            for (int l = 0, r = k - 1; l < r; l++, r--) {
                int tmp = sim[l];
                sim[l] = sim[r];
                sim[r] = tmp;
            }
        }
        Arrays.sort(orig);
        if (!Arrays.equals(sim, orig)) {
            return "Array is not sorted after applying flips";
        }
        return true;
    }
}
