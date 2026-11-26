class WordDictionary {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd;
    }

    private final Node root;

    public WordDictionary() {
        root = new Node();
    }

    public void addWord(String word) {
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

    public boolean search(String word) {
        return dfs(word, 0, root);
    }

    private boolean dfs(String word, int index, Node node) {
        if (index == word.length()) {
            return node.isEnd;
        }
        char ch = word.charAt(index);
        if (ch == '.') {
            for (Node child : node.children) {
                if (child != null && dfs(word, index + 1, child)) {
                    return true;
                }
            }
            return false;
        }
        Node next = node.children[ch - 'a'];
        return next != null && dfs(word, index + 1, next);
    }
}
