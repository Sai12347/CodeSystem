class Node {
    int val;
    Node next;
    Node random;

    public Node(int val) {
        this.val = val;
        this.next = null;
        this.random = null;
    }
}

class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> spec = (List<Object>) inp.get("head");
        int n = spec.size();
        Node[] orig = new Node[n];
        int[] origVals = new int[n];
        Integer[] origRandIdx = new Integer[n];

        for (int i = 0; i < n; i++) {
            List<Object> pair = (List<Object>) spec.get(i);
            origVals[i] = ((Number) pair.get(0)).intValue();
            origRandIdx[i] = pair.get(1) == null ? null : ((Number) pair.get(1)).intValue();
            orig[i] = new Node(origVals[i]);
        }
        for (int i = 0; i < n - 1; i++) {
            orig[i].next = orig[i + 1];
        }
        for (int i = 0; i < n; i++) {
            orig[i].random = origRandIdx[i] == null ? null : orig[origRandIdx[i]];
        }

        Node origHead = n > 0 ? orig[0] : null;
        IdentityHashMap<Node, Boolean> origSet = new IdentityHashMap<>();
        for (Node node : orig) {
            origSet.put(node, Boolean.TRUE);
        }

        Node ans = new Solution().copyRandomList(origHead);

        // Verify original list was not corrupted
        Node cur = origHead;
        for (int i = 0; i < n; i++) {
            Node expectedRand = origRandIdx[i] == null ? null : orig[origRandIdx[i]];
            if (cur != orig[i] || cur.val != origVals[i] || cur.random != expectedRand) {
                return "ERROR: original linked list was modified";
            }
            cur = cur.next;
        }
        if (cur != null) {
            return "ERROR: original linked list length was modified";
        }

        // Walk and validate copied list
        List<Node> copied = new ArrayList<>();
        IdentityHashMap<Node, Integer> copyIdx = new IdentityHashMap<>();
        cur = ans;
        while (cur != null) {
            if (origSet.containsKey(cur)) {
                return "ERROR: returned list shares a node reference with the original list";
            }
            if (copyIdx.containsKey(cur)) {
                return "ERROR: returned list contains a cycle";
            }
            if (copied.size() > n) {
                return "ERROR: returned list is longer than input";
            }
            copyIdx.put(cur, copied.size());
            copied.add(cur);
            cur = cur.next;
        }

        List<Object> out = new ArrayList<>(copied.size());
        for (Node node : copied) {
            Object ridx;
            if (node.random == null) {
                ridx = null;
            } else {
                Integer idx = copyIdx.get(node.random);
                if (idx == null) {
                    return "ERROR: random pointer does not point to a node in the copied list";
                }
                ridx = (long) idx;
            }
            List<Object> entry = new ArrayList<>(2);
            entry.add((long) node.val);
            entry.add(ridx);
            out.add(entry);
        }
        return out;
    }
}
