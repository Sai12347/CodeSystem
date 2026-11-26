interface NestedInteger {
    boolean isInteger();
    Integer getInteger();
    List<NestedInteger> getList();
}

class NestedIntegerImpl implements NestedInteger {
    private final Integer intVal;
    private final List<NestedInteger> listVal;

    @SuppressWarnings("unchecked")
    NestedIntegerImpl(Object raw) {
        if (raw instanceof Number) {
            this.intVal = ((Number) raw).intValue();
            this.listVal = null;
        } else {
            this.intVal = null;
            List<Object> items = (List<Object>) raw;
            List<NestedInteger> built = new ArrayList<>(items.size());
            for (Object item : items) {
                built.add(new NestedIntegerImpl(item));
            }
            this.listVal = built;
        }
    }

    @Override
    public boolean isInteger() {
        return intVal != null;
    }

    @Override
    public Integer getInteger() {
        return intVal;
    }

    @Override
    public List<NestedInteger> getList() {
        return listVal;
    }
}

class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> raw = (List<Object>) inp.get("nestedList");
        List<NestedInteger> nestedList = new ArrayList<>(raw.size());
        for (Object item : raw) {
            nestedList.add(new NestedIntegerImpl(item));
        }
        NestedIterator it = new NestedIterator(nestedList);
        List<Integer> res = new ArrayList<>();
        int limit = 100000;
        while (it.hasNext()) {
            if (res.size() >= limit) {
                return "Exceeded maximum output length (possible infinite loop in hasNext/next)";
            }
            if (!it.hasNext()) {
                return "hasNext() is not idempotent";
            }
            res.add(it.next());
        }
        if (it.hasNext()) {
            return "hasNext() returned true after iterator was exhausted";
        }
        return res;
    }
}
