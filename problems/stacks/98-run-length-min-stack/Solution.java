class RunLengthMinStack {
    private final List<long[]> runs = new ArrayList<>(); // {val, count, runningMin}

    public RunLengthMinStack() {
    }

    public void pushMany(int val, int count) {
        if (!runs.isEmpty() && runs.get(runs.size() - 1)[0] == val) {
            runs.get(runs.size() - 1)[1] += count;
        } else {
            long mn = runs.isEmpty() ? val : Math.min((long) val, runs.get(runs.size() - 1)[2]);
            runs.add(new long[]{val, count, mn});
        }
    }

    public long popMany(int count) {
        long total = 0L;
        long rem = count;
        while (rem > 0) {
            long[] entry = runs.get(runs.size() - 1);
            if (entry[1] <= rem) {
                total += entry[0] * entry[1];
                rem -= entry[1];
                runs.remove(runs.size() - 1);
            } else {
                total += entry[0] * rem;
                entry[1] -= rem;
                rem = 0;
            }
        }
        return total;
    }

    public int top() {
        return (int) runs.get(runs.size() - 1)[0];
    }

    public int getMin() {
        return (int) runs.get(runs.size() - 1)[2];
    }
}
