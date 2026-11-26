class TextEditor {
    private static class Node {
        final char ch;
        Node prev;
        Node next;

        Node(char ch) {
            this.ch = ch;
        }
    }

    private final Node head;
    private final Node tail;
    private Node cursor;

    public TextEditor() {
        head = new Node(' ');
        tail = new Node(' ');
        head.next = tail;
        tail.prev = head;
        cursor = head;
    }

    private String leftPreview() {
        StringBuilder sb = new StringBuilder(10);
        Node p = cursor;
        for (int i = 0; i < 10 && p != head; i++) {
            sb.append(p.ch);
            p = p.prev;
        }
        return sb.reverse().toString();
    }

    public void addText(String text) {
        for (int i = 0; i < text.length(); i++) {
            Node node = new Node(text.charAt(i));
            Node nxt = cursor.next;
            cursor.next = node;
            node.prev = cursor;
            node.next = nxt;
            nxt.prev = node;
            cursor = node;
        }
    }

    public int deleteText(int k) {
        int deleted = 0;
        while (deleted < k && cursor != head) {
            Node prev = cursor.prev;
            Node nxt = cursor.next;
            prev.next = nxt;
            nxt.prev = prev;
            cursor = prev;
            deleted++;
        }
        return deleted;
    }

    public String cursorLeft(int k) {
        while (k > 0 && cursor != head) {
            cursor = cursor.prev;
            k--;
        }
        return leftPreview();
    }

    public String cursorRight(int k) {
        while (k > 0 && cursor.next != tail) {
            cursor = cursor.next;
            k--;
        }
        return leftPreview();
    }
}
