class Trie {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd;
    }

    private final Node root;

    public Trie() {
        root = new Node();
    }

    public void insert(String word) {
        Node cur = root;
        for (int i = 0; i < word.length(); i++) {
            int idx = word.charAt(i) - 'a';
            if (cur.children[idx] == null) {
                cur.children[idx] = new Node();
            }
            cur = cur.children[idx];
        }
        cur.isEnd = true;
    }

    private Node find(String text) {
        Node cur = root;
        for (int i = 0; i < text.length(); i++) {
            int idx = text.charAt(i) - 'a';
            cur = cur.children[idx];
            if (cur == null) {
                return null;
            }
        }
        return cur;
    }

    public boolean search(String word) {
        Node node = find(word);
        return node != null && node.isEnd;
    }

    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }
}
