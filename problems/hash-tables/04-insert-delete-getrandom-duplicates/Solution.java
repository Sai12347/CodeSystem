class RandomizedCollection {
    private final List<Integer> vals = new ArrayList<>();
    private final Map<Integer, LinkedHashSet<Integer>> pos = new HashMap<>();
    private final Random rand = new Random();

    public RandomizedCollection() {
    }

    public boolean insert(int val) {
        LinkedHashSet<Integer> idxs = pos.computeIfAbsent(val, k -> new LinkedHashSet<>());
        boolean wasAbsent = idxs.isEmpty();
        idxs.add(vals.size());
        vals.add(val);
        return wasAbsent;
    }

    public boolean remove(int val) {
        LinkedHashSet<Integer> idxs = pos.get(val);
        if (idxs == null || idxs.isEmpty()) {
            return false;
        }
        Iterator<Integer> it = idxs.iterator();
        int removeIdx = it.next();
        it.remove();
        int lastIdx = vals.size() - 1;
        int lastVal = vals.get(lastIdx);
        if (removeIdx != lastIdx) {
            vals.set(removeIdx, lastVal);
            LinkedHashSet<Integer> lastIdxs = pos.get(lastVal);
            lastIdxs.remove(lastIdx);
            lastIdxs.add(removeIdx);
        }
        vals.remove(lastIdx);
        if (idxs.isEmpty()) {
            pos.remove(val);
        }
        return true;
    }

    public int getRandom() {
        return vals.get(rand.nextInt(vals.size()));
    }
}
