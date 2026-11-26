class MyLinkedList {
    private static class Node {
        int val;
        Node prev;
        Node next;

        Node(int val) {
            this.val = val;
        }
    }

    private final Node head;
    private final Node tail;
    private int size;

    public MyLinkedList() {
        head = new Node(0);
        tail = new Node(0);
        head.next = tail;
        tail.prev = head;
        size = 0;
    }

    private Node nodeAt(int index) {
        Node curr;
        if (index < size / 2) {
            curr = head.next;
            for (int i = 0; i < index; i++) {
                curr = curr.next;
            }
        } else {
            curr = tail.prev;
            for (int i = size - 1; i > index; i--) {
                curr = curr.prev;
            }
        }
        return curr;
    }

    private void insertBefore(Node target, int val) {
        Node node = new Node(val);
        Node prev = target.prev;
        prev.next = node;
        node.prev = prev;
        node.next = target;
        target.prev = node;
        size++;
    }

    public int get(int index) {
        if (index < 0 || index >= size) {
            return -1;
        }
        return nodeAt(index).val;
    }

    public void addAtHead(int val) {
        insertBefore(head.next, val);
    }

    public void addAtTail(int val) {
        insertBefore(tail, val);
    }

    public void addAtIndex(int index, int val) {
        if (index < 0 || index > size) {
            return;
        }
        if (index == size) {
            insertBefore(tail, val);
        } else {
            insertBefore(nodeAt(index), val);
        }
    }

    public void deleteAtIndex(int index) {
        if (index < 0 || index >= size) {
            return;
        }
        Node node = nodeAt(index);
        node.prev.next = node.next;
        node.next.prev = node.prev;
        size--;
    }
}
