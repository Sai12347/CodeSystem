class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> raw = (List<Object>) inp.get("nums");
        int n = raw.size();
        int[] orig = new int[n];
        int[] copy = new int[n];
        for (int i = 0; i < n; i++) {
            orig[i] = ((Number) raw.get(i)).intValue();
            copy[i] = orig[i];
        }
        int idx = new Solution().findPeakElement(copy);
        if (idx < 0 || idx >= n) {
            return "Index " + idx + " out of range [0, " + (n - 1) + "]";
        }
        boolean leftOk = idx == 0 || orig[idx] > orig[idx - 1];
        boolean rightOk = idx == n - 1 || orig[idx] > orig[idx + 1];
        if (!leftOk || !rightOk) {
            return "Index " + idx + " (value " + orig[idx] + ") is not a peak";
        }
        return true;
    }
}
