class Solution {
    public ListNode reverseEvenLengthGroups(ListNode head) {
        ListNode prev = head;
        int groupLen = 2;
        while (prev.next != null) {
            ListNode node = prev;
            int count = 0;
            while (count < groupLen && node.next != null) {
                node = node.next;
                count++;
            }
            if (count % 2 == 0) {
                ListNode groupHead = prev.next;
                ListNode nxtGroup = node.next;
                ListNode rprev = nxtGroup;
                ListNode curr = groupHead;
                for (int i = 0; i < count; i++) {
                    ListNode nxt = curr.next;
                    curr.next = rprev;
                    rprev = curr;
                    curr = nxt;
                }
                prev.next = rprev;
                prev = groupHead;
            } else {
                prev = node;
            }
            groupLen++;
        }
        return head;
    }
}
