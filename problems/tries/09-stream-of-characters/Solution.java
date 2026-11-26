class StreamChecker {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd;
    }

    private final Node root;
    private final char[] ring;
    private int size;
    private int head;

    public StreamChecker(String[] words) {
        root = new Node();
        int maxLen = 0;
        for (String word : words) {
            if (word.length() > maxLen) {
                maxLen = word.length();
            }
            Node cur = root;
            for (int i = word.length() - 1; i >= 0; i--) {
                int idx = word.charAt(i) - 'a';
                if (cur.children[idx] == null) {
                    cur.children[idx] = new Node();
                }
                cur = cur.children[idx];
            }
            cur.isEnd = true;
        }
        ring = new char[Math.max(1, maxLen)];
        size = 0;
        head = 0;
    }

    public boolean query(char letter) {
        ring[head] = letter;
        int pos = head;
        head = (head + 1) % ring.length;
        if (size < ring.length) {
            size++;
        }
        Node cur = root;
        for (int step = 0; step < size; step++) {
            cur = cur.children[ring[pos] - 'a'];
            if (cur == null) {
                return false;
            }
            if (cur.isEnd) {
                return true;
            }
            pos = (pos == 0) ? ring.length - 1 : pos - 1;
        }
        return false;
    }
}
