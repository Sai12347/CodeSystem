class Solution {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd;
    }

    public List<String> findAllConcatenatedWordsInADict(String[] words) {
        Arrays.sort(words, Comparator.comparingInt(String::length));
        Node root = new Node();
        List<String> result = new ArrayList<>();

        for (String w : words) {
            if (w.isEmpty()) {
                continue;
            }
            boolean[] visited = new boolean[w.length() + 1];
            if (canForm(w, 0, root, visited)) {
                result.add(w);
            } else {
                insert(root, w);
            }
        }
        return result;
    }

    private boolean canForm(String w, int start, Node root, boolean[] visited) {
        int n = w.length();
        if (start == n) {
            return true;
        }
        if (visited[start]) {
            return false;
        }
        visited[start] = true;
        Node cur = root;
        for (int i = start; i < n; i++) {
            cur = cur.children[w.charAt(i) - 'a'];
            if (cur == null) {
                break;
            }
            if (cur.isEnd && canForm(w, i + 1, root, visited)) {
                return true;
            }
        }
        return false;
    }

    private void insert(Node root, String w) {
        Node cur = root;
        for (int i = 0; i < w.length(); i++) {
            int idx = w.charAt(i) - 'a';
            if (cur.children[idx] == null) {
                cur.children[idx] = new Node();
            }
            cur = cur.children[idx];
        }
        cur.isEnd = true;
    }
}
