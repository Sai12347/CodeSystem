class Solution {
    private ListNode intersectTwo(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (a != null && b != null) {
            if (a.val == b.val) {
                tail.next = a;
                tail = tail.next;
                a = a.next;
                b = b.next;
            } else if (a.val < b.val) {
                a = a.next;
            } else {
                b = b.next;
            }
        }
        tail.next = null;
        return dummy.next;
    }

    public ListNode commonElementsKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) {
            return null;
        }
        int minIdx = 0;
        int minLen = Integer.MAX_VALUE;
        for (int i = 0; i < lists.length; i++) {
            int len = 0;
            for (ListNode curr = lists[i]; curr != null; curr = curr.next) {
                len++;
            }
            if (len == 0) {
                return null;
            }
            if (len < minLen) {
                minLen = len;
                minIdx = i;
            }
        }
        ListNode res = lists[minIdx];
        for (int i = 0; i < lists.length; i++) {
            if (i == minIdx) {
                continue;
            }
            res = intersectTwo(res, lists[i]);
            if (res == null) {
                return null;
            }
        }
        return res;
    }
}
