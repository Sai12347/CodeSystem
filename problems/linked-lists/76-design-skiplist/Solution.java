class Skiplist {
    private static final int MAX_LEVEL = 16;

    private static class Node {
        int val;
        Node[] forward;
        Node(int val, int level) {
            this.val = val;
            this.forward = new Node[level];
        }
    }

    private final Node head = new Node(Integer.MIN_VALUE, MAX_LEVEL);
    private int level = 1;
    private final Random rng = new Random(42);

    public Skiplist() {
    }

    private int randomLevel() {
        int lvl = 1;
        while (lvl < MAX_LEVEL && rng.nextBoolean()) {
            lvl++;
        }
        return lvl;
    }

    public boolean search(int target) {
        Node curr = head;
        for (int i = level - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < target) {
                curr = curr.forward[i];
            }
        }
        Node cand = curr.forward[0];
        return cand != null && cand.val == target;
    }

    public void add(int num) {
        Node[] update = new Node[MAX_LEVEL];
        Arrays.fill(update, head);
        Node curr = head;
        for (int i = level - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < num) {
                curr = curr.forward[i];
            }
            update[i] = curr;
        }
        int lvl = randomLevel();
        if (lvl > level) {
            level = lvl;
        }
        Node node = new Node(num, lvl);
        for (int i = 0; i < lvl; i++) {
            node.forward[i] = update[i].forward[i];
            update[i].forward[i] = node;
        }
    }

    public boolean erase(int num) {
        Node[] update = new Node[MAX_LEVEL];
        Arrays.fill(update, head);
        Node curr = head;
        for (int i = level - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < num) {
                curr = curr.forward[i];
            }
            update[i] = curr;
        }
        Node target = curr.forward[0];
        if (target == null || target.val != num) {
            return false;
        }
        for (int i = 0; i < target.forward.length; i++) {
            if (update[i].forward[i] == target) {
                update[i].forward[i] = target.forward[i];
            }
        }
        while (level > 1 && head.forward[level - 1] == null) {
            level--;
        }
        return true;
    }
}
