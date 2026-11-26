class TopKMinStack {
    private final List<int[]> up = new ArrayList<>();
    private final List<Integer> prefMin = new ArrayList<>();

    public TopKMinStack() {
    }

    public void push(int val) {
        int idx = up.size();
        int len = 32 - Integer.numberOfLeadingZeros(idx + 1);
        int[] row = new int[len];
        row[0] = val;
        for (int j = 1; j < len; j++) {
            row[j] = Math.min(row[j - 1], up.get(idx - (1 << (j - 1)))[j - 1]);
        }
        up.add(row);
        int mn = prefMin.isEmpty() ? val : Math.min(val, prefMin.get(prefMin.size() - 1));
        prefMin.add(mn);
    }

    public int pop() {
        prefMin.remove(prefMin.size() - 1);
        return up.remove(up.size() - 1)[0];
    }

    public int getMin() {
        return prefMin.get(prefMin.size() - 1);
    }

    public int getTopKMin(int k) {
        int n = up.size();
        int p = 31 - Integer.numberOfLeadingZeros(k);
        int a = up.get(n - 1)[p];
        int b = up.get(n - k + (1 << p) - 1)[p];
        return Math.min(a, b);
    }
}
