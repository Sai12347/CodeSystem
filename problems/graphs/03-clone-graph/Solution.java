class Solution {
    public Node cloneGraph(Node node) {
        if (node == null) {
            return null;
        }
        Map<Node, Node> clones = new HashMap<>();
        return dfs(node, clones);
    }

    private Node dfs(Node cur, Map<Node, Node> clones) {
        Node existing = clones.get(cur);
        if (existing != null) {
            return existing;
        }
        Node copy = new Node(cur.val);
        clones.put(cur, copy);
        for (Node nb : cur.neighbors) {
            copy.neighbors.add(dfs(nb, clones));
        }
        return copy;
    }
}
