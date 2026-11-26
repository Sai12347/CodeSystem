class TransactionalStack {
    private static class UndoNode {
        boolean pushUndo;
        int val;
        UndoNode next;
        UndoNode(boolean pushUndo, int val, UndoNode next) {
            this.pushUndo = pushUndo;
            this.val = val;
            this.next = next;
        }
    }

    private final Deque<int[]> st = new ArrayDeque<>();
    private final Deque<UndoNode[]> tx = new ArrayDeque<>();

    public TransactionalStack() {}

    private void rawPush(int val) {
        int mn = st.isEmpty() ? val : Math.min(val, st.peek()[1]);
        st.push(new int[]{val, mn});
    }

    private int rawPop() {
        return st.pop()[0];
    }

    private void record(boolean pushUndo, int val) {
        if (!tx.isEmpty()) {
            UndoNode[] frame = tx.peek();
            UndoNode node = new UndoNode(pushUndo, val, frame[0]);
            frame[0] = node;
            if (frame[1] == null) frame[1] = node;
        }
    }

    public void push(int val) {
        rawPush(val);
        record(false, 0);
    }

    public int pop() {
        int val = rawPop();
        record(true, val);
        return val;
    }

    public int top() {
        return st.peek()[0];
    }

    public int getMin() {
        return st.peek()[1];
    }

    public void begin() {
        tx.push(new UndoNode[]{null, null});
    }

    public boolean rollback() {
        if (tx.isEmpty()) return false;
        UndoNode cur = tx.pop()[0];
        while (cur != null) {
            if (cur.pushUndo) rawPush(cur.val);
            else rawPop();
            cur = cur.next;
        }
        return true;
    }

    public boolean commit() {
        if (tx.isEmpty()) return false;
        UndoNode[] child = tx.pop();
        if (!tx.isEmpty() && child[0] != null) {
            UndoNode[] parent = tx.peek();
            child[1].next = parent[0];
            parent[0] = child[0];
            if (parent[1] == null) parent[1] = child[1];
        }
        return true;
    }
}
