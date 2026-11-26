class MinDeque {
    private final List<Integer> lv = new ArrayList<>();
    private final List<Integer> lm = new ArrayList<>();
    private final List<Integer> rv = new ArrayList<>();
    private final List<Integer> rm = new ArrayList<>();

    public MinDeque() {
    }

    private void pushSide(List<Integer> vs, List<Integer> ms, int val) {
        vs.add(val);
        int mn = ms.isEmpty() ? val : Math.min(val, ms.get(ms.size() - 1));
        ms.add(mn);
    }

    private void rebalance(List<Integer> srcV, List<Integer> srcM, List<Integer> dstV, List<Integer> dstM) {
        int m = srcV.size();
        int half = (m + 1) / 2;
        int[] tmp = new int[m];
        for (int i = 0; i < m; i++) tmp[i] = srcV.get(i);
        srcV.clear();
        srcM.clear();
        for (int i = half - 1; i >= 0; i--) {
            pushSide(dstV, dstM, tmp[i]);
        }
        for (int i = half; i < m; i++) {
            pushSide(srcV, srcM, tmp[i]);
        }
    }

    public void pushFront(int val) {
        pushSide(lv, lm, val);
    }

    public void pushBack(int val) {
        pushSide(rv, rm, val);
    }

    public int popFront() {
        if (lv.isEmpty()) rebalance(rv, rm, lv, lm);
        lm.remove(lm.size() - 1);
        return lv.remove(lv.size() - 1);
    }

    public int popBack() {
        if (rv.isEmpty()) rebalance(lv, lm, rv, rm);
        rm.remove(rm.size() - 1);
        return rv.remove(rv.size() - 1);
    }

    public int getMin() {
        if (!lm.isEmpty() && !rm.isEmpty()) {
            return Math.min(lm.get(lm.size() - 1), rm.get(rm.size() - 1));
        }
        return !lm.isEmpty() ? lm.get(lm.size() - 1) : rm.get(rm.size() - 1);
    }
}
