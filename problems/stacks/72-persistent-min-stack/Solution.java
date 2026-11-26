class PersistentMinStack {
    private final List<Integer> val = new ArrayList<>();
    private final List<Integer> minVal = new ArrayList<>();
    private final List<Integer> parent = new ArrayList<>();
    private final List<Integer> verNode = new ArrayList<>();

    public PersistentMinStack() {
        val.add(0);
        minVal.add(0);
        parent.add(0);
        verNode.add(0);
    }

    public int push(int version, int x) {
        int p = verNode.get(version);
        int mn = (p == 0) ? x : Math.min(x, minVal.get(p));
        int nodeId = val.size();
        val.add(x);
        minVal.add(mn);
        parent.add(p);
        verNode.add(nodeId);
        return verNode.size() - 1;
    }

    public int pop(int version) {
        int p = verNode.get(version);
        verNode.add(parent.get(p));
        return verNode.size() - 1;
    }

    public int top(int version) {
        return val.get(verNode.get(version));
    }

    public int getMin(int version) {
        return minVal.get(verNode.get(version));
    }
}
