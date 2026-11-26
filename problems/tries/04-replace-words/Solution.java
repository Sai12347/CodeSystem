class Solution {
    private static class Node {
        Node[] children = new Node[26];
        boolean isEnd;
    }

    public String replaceWords(List<String> dictionary, String sentence) {
        Node root = new Node();
        for (String w : dictionary) {
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

        String[] words = sentence.split(" ");
        StringBuilder sb = new StringBuilder(sentence.length());
        for (int i = 0; i < words.length; i++) {
            if (i > 0) {
                sb.append(' ');
            }
            String w = words[i];
            Node cur = root;
            int endIdx = -1;
            for (int j = 0; j < w.length(); j++) {
                cur = cur.children[w.charAt(j) - 'a'];
                if (cur == null) {
                    break;
                }
                if (cur.isEnd) {
                    endIdx = j + 1;
                    break;
                }
            }
            if (endIdx != -1) {
                sb.append(w, 0, endIdx);
            } else {
                sb.append(w);
            }
        }
        return sb.toString();
    }
}
