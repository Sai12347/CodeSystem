class MagicDictionary {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd;
    }

    private Node root;

    public MagicDictionary() {
        root = new Node();
    }

    public void buildDict(String[] dictionary) {
        root = new Node();
        for (String word : dictionary) {
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
    }

    public boolean search(String searchWord) {
        return dfs(searchWord, 0, root, false);
    }

    private boolean dfs(String word, int index, Node node, boolean modified) {
        if (index == word.length()) {
            return modified && node.isEnd;
        }
        int idx = word.charAt(index) - 'a';
        if (node.children[idx] != null && dfs(word, index + 1, node.children[idx], modified)) {
            return true;
        }
        if (!modified) {
            for (int i = 0; i < 26; i++) {
                if (i != idx && node.children[i] != null && dfs(word, index + 1, node.children[i], true)) {
                    return true;
                }
            }
        }
        return false;
    }
}
