class Node {
    public int val;
    public List<Node> neighbors;

    public Node() {
        val = 0;
        neighbors = new ArrayList<Node>();
    }

    public Node(int _val) {
        val = _val;
        neighbors = new ArrayList<Node>();
    }

    public Node(int _val, ArrayList<Node> _neighbors) {
        val = _val;
        neighbors = _neighbors;
    }
}

class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> adjObj = (List<Object>) inp.get("adjList");
        int n = adjObj.size();

        Node[] orig = new Node[n];
        for (int i = 0; i < n; i++) {
            orig[i] = new Node(i + 1);
        }

        List<List<Node>> expectedOrigNbs = new ArrayList<>(n);
        for (int i = 0; i < n; i++) {
            List<Object> row = (List<Object>) adjObj.get(i);
            List<Node> snap = new ArrayList<>(row.size());
            for (Object vObj : row) {
                int v = ((Number) vObj).intValue();
                orig[i].neighbors.add(orig[v - 1]);
                snap.add(orig[v - 1]);
            }
            expectedOrigNbs.add(snap);
        }

        Node origStart = n > 0 ? orig[0] : null;
        IdentityHashMap<Node, Boolean> origSet = new IdentityHashMap<>();
        for (Node node : orig) {
            origSet.put(node, Boolean.TRUE);
        }

        Node ans = new Solution().cloneGraph(origStart);

        // Verify original graph was not modified
        for (int i = 0; i < n; i++) {
            if (orig[i].val != i + 1) {
                return "ERROR: original graph node value was modified";
            }
            List<Node> snap = expectedOrigNbs.get(i);
            if (orig[i].neighbors == null || orig[i].neighbors.size() != snap.size()) {
                return "ERROR: original graph neighbors were modified";
            }
            for (int j = 0; j < snap.size(); j++) {
                if (orig[i].neighbors.get(j) != snap.get(j)) {
                    return "ERROR: original graph neighbor reference was modified";
                }
            }
        }

        if (n == 0) {
            if (ans != null) {
                return "ERROR: expected null for empty graph";
            }
            return new ArrayList<Object>();
        }

        if (ans == null) {
            return "ERROR: returned null for non-empty graph";
        }
        if (origSet.containsKey(ans)) {
            return "ERROR: returned graph shares a node reference with the original graph";
        }
        if (ans.val != 1) {
            return "ERROR: starting cloned node must have val 1";
        }

        IdentityHashMap<Node, Boolean> visited = new IdentityHashMap<>();
        Node[] byVal = new Node[n + 1];
        int uniqueVals = 0;
        ArrayDeque<Node> q = new ArrayDeque<>();
        visited.put(ans, Boolean.TRUE);
        q.add(ans);

        while (!q.isEmpty()) {
            Node cur = q.poll();
            if (origSet.containsKey(cur)) {
                return "ERROR: cloned graph shares a node reference with the original graph";
            }
            if (cur.val < 1 || cur.val > n) {
                return "ERROR: cloned node has out-of-range value";
            }
            if (byVal[cur.val] != null && byVal[cur.val] != cur) {
                return "ERROR: duplicate cloned nodes created for the same value";
            }
            if (byVal[cur.val] == null) {
                byVal[cur.val] = cur;
                uniqueVals++;
            }
            if (cur.neighbors == null) {
                return "ERROR: cloned node has null neighbors list";
            }
            for (Node nb : cur.neighbors) {
                if (nb == null) {
                    return "ERROR: cloned node contains a null neighbor";
                }
                if (origSet.containsKey(nb)) {
                    return "ERROR: cloned node references an original node";
                }
                if (!visited.containsKey(nb)) {
                    if (visited.size() >= n) {
                        return "ERROR: cloned graph contains more nodes than the original graph";
                    }
                    visited.put(nb, Boolean.TRUE);
                    q.add(nb);
                }
            }
        }

        if (uniqueVals != n) {
            return "ERROR: cloned graph does not contain all nodes";
        }

        List<Object> out = new ArrayList<>(n);
        for (int v = 1; v <= n; v++) {
            List<Node> nbs = byVal[v].neighbors;
            List<Long> vals = new ArrayList<>(nbs.size());
            for (Node nb : nbs) {
                vals.add((long) nb.val);
            }
            Collections.sort(vals);
            out.add(vals);
        }
        return out;
    }
}
