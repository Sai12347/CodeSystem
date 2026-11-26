class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> raw = (List<Object>) inp.get("nums");
        int n = raw.size();
        int[] orig = new int[n];
        int[] arr = new int[n];
        for (int i = 0; i < n; i++) {
            orig[i] = ((Number) raw.get(i)).intValue();
            arr[i] = orig[i];
        }
        new Solution().wiggleSort(arr);
        int[] sOrig = orig.clone();
        int[] sArr = arr.clone();
        Arrays.sort(sOrig);
        Arrays.sort(sArr);
        if (!Arrays.equals(sOrig, sArr)) {
            return "Output array is not a permutation of the input array";
        }
        for (int i = 0; i < n - 1; i++) {
            if (i % 2 == 0) {
                if (!(arr[i] < arr[i + 1])) {
                    return "Wiggle condition failed at index " + i + ": " + arr[i] + " is not < " + arr[i + 1];
                }
            } else {
                if (!(arr[i] > arr[i + 1])) {
                    return "Wiggle condition failed at index " + i + ": " + arr[i] + " is not > " + arr[i + 1];
                }
            }
        }
        return true;
    }
}
