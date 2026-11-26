class FreqStack {
    private final Map<Integer, Integer> freq = new HashMap<>();
    private final Map<Integer, Deque<Integer>> group = new HashMap<>();
    private int maxFreq = 0;

    public FreqStack() {}

    public void push(int val) {
        int f = freq.getOrDefault(val, 0) + 1;
        freq.put(val, f);
        if (f > maxFreq) maxFreq = f;
        group.computeIfAbsent(f, k -> new ArrayDeque<>()).push(val);
    }

    public int pop() {
        Deque<Integer> st = group.get(maxFreq);
        int val = st.pop();
        freq.put(val, freq.get(val) - 1);
        if (st.isEmpty()) maxFreq--;
        return val;
    }
}
