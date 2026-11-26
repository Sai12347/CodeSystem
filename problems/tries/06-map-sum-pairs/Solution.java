class MapSum {
    private static class Node {
        Node[] children = new Node[26];
        int score;
    }

    private final Node root;
    private final Map<String, Integer> values;

    public MapSum() {
        root = new Node();
        values = new HashMap<>();
    }

    public void insert(String key, int val) {
        int delta = val - values.getOrDefault(key, 0);
        values.put(key, val);
        Node cur = root;
        for (int i = 0; i < key.length(); i++) {
            int idx = key.charAt(i) - 'a';
            if (cur.children[idx] == null) {
                cur.children[idx] = new Node();
            }
            cur = cur.children[idx];
            cur.score += delta;
        }
    }

    public int sum(String prefix) {
        Node cur = root;
        for (int i = 0; i < prefix.length(); i++) {
            cur = cur.children[prefix.charAt(i) - 'a'];
            if (cur == null) {
                return 0;
            }
        }
        return cur.score;
    }
}
