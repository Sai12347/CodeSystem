class RandomizedSet {
    private final List<Integer> vals = new ArrayList<>();
    private final Map<Integer, Integer> pos = new HashMap<>();
    private final Random rand = new Random();

    public RandomizedSet() {
    }

    public boolean insert(int val) {
        if (pos.containsKey(val)) {
            return false;
        }
        pos.put(val, vals.size());
        vals.add(val);
        return true;
    }

    public boolean remove(int val) {
        Integer idxObj = pos.remove(val);
        if (idxObj == null) {
            return false;
        }
        int idx = idxObj;
        int last = vals.remove(vals.size() - 1);
        if (idx < vals.size()) {
            vals.set(idx, last);
            pos.put(last, idx);
        }
        return true;
    }

    public int getRandom() {
        return vals.get(rand.nextInt(vals.size()));
    }
}
