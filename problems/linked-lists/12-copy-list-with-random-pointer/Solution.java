class Solution {
    public Node copyRandomList(Node head) {
        if (head == null) {
            return null;
        }

        // Pass 1: interleave cloned nodes right after each original node
        Node cur = head;
        while (cur != null) {
            Node clone = new Node(cur.val);
            clone.next = cur.next;
            cur.next = clone;
            cur = clone.next;
        }

        // Pass 2: assign random pointers for cloned nodes
        cur = head;
        while (cur != null) {
            if (cur.random != null) {
                cur.next.random = cur.random.next;
            }
            cur = cur.next.next;
        }

        // Pass 3: separate original list and cloned list
        Node cloneHead = head.next;
        cur = head;
        while (cur != null) {
            Node clone = cur.next;
            cur.next = clone.next;
            if (clone.next != null) {
                clone.next = clone.next.next;
            }
            cur = cur.next;
        }

        return cloneHead;
    }
}
