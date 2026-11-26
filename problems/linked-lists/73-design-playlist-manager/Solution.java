class PlaylistManager {
    private static class Node {
        int songId;
        Node prev, next;
        Node(int songId) {
            this.songId = songId;
        }
    }

    private final Node head = new Node(0);
    private final Node tail = new Node(0);
    private final Map<Integer, Node> nodes = new HashMap<>();
    private Node curr = null;

    public PlaylistManager() {
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertAfter(Node ref, Node node) {
        node.prev = ref;
        node.next = ref.next;
        ref.next.prev = node;
        ref.next = node;
    }

    public void addSong(int songId) {
        if (nodes.containsKey(songId)) {
            return;
        }
        Node node = new Node(songId);
        insertAfter(tail.prev, node);
        nodes.put(songId, node);
        if (curr == null) {
            curr = node;
        }
    }

    public void playNext() {
        if (curr != null && curr.next != tail) {
            curr = curr.next;
        }
    }

    public void playPrev() {
        if (curr != null && curr.prev != head) {
            curr = curr.prev;
        }
    }

    public void removeSong(int songId) {
        Node node = nodes.remove(songId);
        if (node == null) {
            return;
        }
        if (curr == node) {
            if (node.next != tail) {
                curr = node.next;
            } else if (node.prev != head) {
                curr = node.prev;
            } else {
                curr = null;
            }
        }
        unlink(node);
    }

    public void moveToFront(int songId) {
        Node node = nodes.get(songId);
        if (node == null) {
            return;
        }
        unlink(node);
        insertAfter(head, node);
    }

    public int getCurrent() {
        return curr != null ? curr.songId : -1;
    }
}
