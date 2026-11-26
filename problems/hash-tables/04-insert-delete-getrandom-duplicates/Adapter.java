class Adapter {
    private static String checkStreak(int streak, Map<Integer, Integer> counts, int total, Map<Integer, Integer> streakCounts) {
        if (streak >= 100 && counts.size() >= 2) {
            if (streakCounts.size() < 2) {
                return "getRandom() returned only " + streakCounts.keySet() + " across " + streak + " draws from " + counts.size() + " distinct values";
            }
            if (streak >= 400) {
                int maxVal = 0;
                int maxCnt = -1;
                for (Map.Entry<Integer, Integer> e : counts.entrySet()) {
                    if (e.getValue() > maxCnt) {
                        maxCnt = e.getValue();
                        maxVal = e.getKey();
                    }
                }
                if ((long) maxCnt * 100 >= 85L * total) {
                    int gotCnt = streakCounts.getOrDefault(maxVal, 0);
                    if ((long) gotCnt * 100 < 70L * streak) {
                        return "getRandom() distribution appears unweighted: value " + maxVal + " has "
                                + maxCnt + "/" + total + " copies but appeared only " + gotCnt + "/" + streak + " times";
                    }
                }
            }
        }
        return null;
    }

    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> ops = (List<Object>) inp.get("ops");
        List<Object> args = (List<Object>) inp.get("args");
        if (ops == null || ops.isEmpty() || !"RandomizedCollection".equals(ops.get(0))) {
            return "First operation must be RandomizedCollection";
        }
        RandomizedCollection obj = new RandomizedCollection();
        Map<Integer, Integer> counts = new HashMap<>();
        int total = 0;
        int streak = 0;
        Map<Integer, Integer> streakCounts = new HashMap<>();

        for (int i = 1; i < ops.size(); i++) {
            String op = (String) ops.get(i);
            List<Object> a = (List<Object>) args.get(i);
            if ("insert".equals(op)) {
                String err = checkStreak(streak, counts, total, streakCounts);
                if (err != null) return err;
                streak = 0;
                streakCounts.clear();
                int val = ((Number) a.get(0)).intValue();
                int prev = counts.getOrDefault(val, 0);
                boolean expected = (prev == 0);
                counts.put(val, prev + 1);
                total++;
                boolean got = obj.insert(val);
                if (got != expected) {
                    return "Op " + i + " insert(" + val + "): expected " + expected + ", got " + got;
                }
            } else if ("remove".equals(op)) {
                String err = checkStreak(streak, counts, total, streakCounts);
                if (err != null) return err;
                streak = 0;
                streakCounts.clear();
                int val = ((Number) a.get(0)).intValue();
                int prev = counts.getOrDefault(val, 0);
                boolean expected = (prev > 0);
                if (expected) {
                    if (prev == 1) counts.remove(val);
                    else counts.put(val, prev - 1);
                    total--;
                }
                boolean got = obj.remove(val);
                if (got != expected) {
                    return "Op " + i + " remove(" + val + "): expected " + expected + ", got " + got;
                }
            } else if ("getRandom".equals(op)) {
                int got = obj.getRandom();
                if (counts.getOrDefault(got, 0) <= 0) {
                    return "Op " + i + " getRandom(): returned " + got + ", which is not in the collection";
                }
                if (counts.size() >= 2) {
                    streak++;
                    streakCounts.put(got, streakCounts.getOrDefault(got, 0) + 1);
                }
            } else {
                return "Unknown operation " + op;
            }
        }
        String err = checkStreak(streak, counts, total, streakCounts);
        if (err != null) return err;
        return true;
    }
}
