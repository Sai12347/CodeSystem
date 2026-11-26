class Solution {
    public ListNode threeWayPartition(ListNode head, int low, int high) {
        ListNode lessD = new ListNode(0);
        ListNode midD = new ListNode(0);
        ListNode highD = new ListNode(0);
        ListNode lessT = lessD;
        ListNode midT = midD;
        ListNode highT = highD;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val < low) {
                lessT.next = curr;
                lessT = curr;
            } else if (curr.val <= high) {
                midT.next = curr;
                midT = curr;
            } else {
                highT.next = curr;
                highT = curr;
            }
            curr = curr.next;
        }
        highT.next = null;
        midT.next = highD.next;
        lessT.next = midD.next;
        return lessD.next;
    }
}
