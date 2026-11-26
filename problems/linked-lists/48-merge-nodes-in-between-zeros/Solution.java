class Solution {
    public ListNode mergeNodes(ListNode head) {
        ListNode write = head;
        ListNode read = head.next;
        int acc = 0;
        while (read != null) {
            if (read.val == 0) {
                write.val = acc;
                acc = 0;
                if (read.next != null) {
                    write = write.next;
                } else {
                    write.next = null;
                }
            } else {
                acc += read.val;
            }
            read = read.next;
        }
        return head;
    }
}
