class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> ops = (List<Object>) inp.get("ops");
        List<Object> args = (List<Object>) inp.get("args");
        if (ops == null || ops.isEmpty() || !"RandomizedSet".equals(ops.get(0))) {
            return "First operation must be RandomizedSet";
        }
        RandomizedSet obj = new RandomizedSet();
        Set<Integer> ref = new HashSet<>();
        int streak = 0;
        Set<Integer> seenInStreak = new HashSet<>();

        for (int i = 1; i < ops.size(); i++) {
            String op = (String) ops.get(i);
            List<Object> a = (List<Object>) args.get(i);
            if ("insert".equals(op)) {
                int val = ((Number) a.get(0)).intValue();
                boolean expected = ref.add(val);
                boolean got = obj.insert(val);
                if (got != expected) {
                    return "Op " + i + " insert(" + val + "): expected " + expected + ", got " + got;
                }
                streak = 0;
                seenInStreak.clear();
            } else if ("remove".equals(op)) {
                int val = ((Number) a.get(0)).intValue();
                boolean expected = ref.remove(val);
                boolean got = obj.remove(val);
                if (got != expected) {
                    return "Op " + i + " remove(" + val + "): expected " + expected + ", got " + got;
                }
                streak = 0;
                seenInStreak.clear();
            } else if ("getRandom".equals(op)) {
                int got = obj.getRandom();
                if (!ref.contains(got)) {
                    return "Op " + i + " getRandom(): returned " + got + ", which is not in the set";
                }
                if (ref.size() >= 2) {
                    streak++;
                    seenInStreak.add(got);
                    if (streak >= 100 && seenInStreak.size() < 2) {
                        return "Op " + i + " getRandom(): returned only " + seenInStreak + " across " + streak + " draws from " + ref.size() + " elements";
                    }
                }
            } else {
                return "Unknown operation " + op;
            }
        }
        return true;
    }
}
