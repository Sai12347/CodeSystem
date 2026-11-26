class Solution {
    private static class Node {
        Node[] children = new Node[26];
        String word;
        int childCount;
    }

    public List<String> findWords(char[][] board, String[] words) {
        Node root = new Node();
        for (String w : words) {
            Node cur = root;
            for (int i = 0; i < w.length(); i++) {
                int idx = w.charAt(i) - 'a';
                if (cur.children[idx] == null) {
                    cur.children[idx] = new Node();
                    cur.childCount++;
                }
                cur = cur.children[idx];
            }
            cur.word = w;
        }

        List<String> result = new ArrayList<>();
        int rows = board.length;
        int cols = board[0].length;
        for (int r = 0; r < rows; r++) {
            for (int c = 0; c < cols; c++) {
                dfs(board, r, c, root, result);
            }
        }
        return result;
    }

    private void dfs(char[][] board, int r, int c, Node parent, List<String> result) {
        char ch = board[r][c];
        if (ch == '#') {
            return;
        }
        int idx = ch - 'a';
        Node node = parent.children[idx];
        if (node == null) {
            return;
        }
        if (node.word != null) {
            result.add(node.word);
            node.word = null;
        }

        board[r][c] = '#';
        if (r > 0) dfs(board, r - 1, c, node, result);
        if (r + 1 < board.length) dfs(board, r + 1, c, node, result);
        if (c > 0) dfs(board, r, c - 1, node, result);
        if (c + 1 < board[0].length) dfs(board, r, c + 1, node, result);
        board[r][c] = ch;

        if (node.childCount == 0 && node.word == null) {
            parent.children[idx] = null;
            parent.childCount--;
        }
    }
}
