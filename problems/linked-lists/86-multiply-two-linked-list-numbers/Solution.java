class Solution {
    public ListNode multiplyLists(ListNode l1, ListNode l2) {
        List<Integer> a = new ArrayList<>();
        for (ListNode c = l1; c != null; c = c.next) {
            a.add(c.val);
        }
        List<Integer> b = new ArrayList<>();
        for (ListNode c = l2; c != null; c = c.next) {
            b.add(c.val);
        }
        Collections.reverse(a);
        Collections.reverse(b);
        if ((a.size() == 1 && a.get(0) == 0) || (b.size() == 1 && b.get(0) == 0)) {
            return new ListNode(0);
        }

        int[] res = new int[a.size() + b.size()];
        for (int i = 0; i < a.size(); i++) {
            int da = a.get(i);
            for (int j = 0; j < b.size(); j++) {
                res[i + j] += da * b.get(j);
            }
        }
        int carry = 0;
        for (int i = 0; i < res.length; i++) {
            int total = res[i] + carry;
            res[i] = total % 10;
            carry = total / 10;
        }
        int top = res.length - 1;
        while (top > 0 && res[top] == 0) {
            top--;
        }
        ListNode head = null;
        for (int i = 0; i <= top; i++) {
            head = new ListNode(res[i], head);
        }
        return head;
    }
}
