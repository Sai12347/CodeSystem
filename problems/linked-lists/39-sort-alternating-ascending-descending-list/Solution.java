class Solution {
    private ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    private ListNode merge(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                tail.next = l1;
                l1 = l1.next;
            } else {
                tail.next = l2;
                l2 = l2.next;
            }
            tail = tail.next;
        }
        tail.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }

    public ListNode sortAlternatingList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode ascHead = head;
        ListNode descHead = head.next;
        ListNode asc = ascHead;
        ListNode desc = descHead;
        while (desc != null && desc.next != null) {
            asc.next = desc.next;
            asc = asc.next;
            desc.next = asc.next;
            desc = desc.next;
        }
        asc.next = null;
        ListNode descSorted = reverse(descHead);
        return merge(ascHead, descSorted);
    }
}
