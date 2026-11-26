class Solution {
    public Node flatten(Node head) {
        Node cur = head;
        while (cur != null) {
            if (cur.child != null) {
                Node nxt = cur.next;
                Node child = cur.child;
                cur.child = null;
                cur.next = child;
                child.prev = cur;

                Node tail = child;
                while (tail.next != null) {
                    tail = tail.next;
                }

                tail.next = nxt;
                if (nxt != null) {
                    nxt.prev = tail;
                }
            }
            cur = cur.next;
        }
        return head;
    }
}
