class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> rawVals = (List<Object>) inp.get("head");
        int pos = ((Number) inp.get("pos")).intValue();
        int n = rawVals.size();
        int[] vals = new int[n];
        ListNode[] nodes = new ListNode[n];
        for (int i = 0; i < n; i++) {
            vals[i] = ((Number) rawVals.get(i)).intValue();
            nodes[i] = new ListNode(vals[i]);
        }
        for (int i = 0; i < n - 1; i++) {
            nodes[i].next = nodes[i + 1];
        }
        if (n > 0 && pos >= 0) {
            nodes[n - 1].next = nodes[pos];
        }
        ListNode head = n > 0 ? nodes[0] : null;
        ListNode ret = new Solution().detectCycle(head);
        for (int i = 0; i < n; i++) {
            if (nodes[i].val != vals[i]) {
                return "linked list values were modified";
            }
            ListNode expectedNext = (i + 1 < n) ? nodes[i + 1] : (pos >= 0 ? nodes[pos] : null);
            if (nodes[i].next != expectedNext) {
                return "linked list next pointers were modified";
            }
        }
        if (ret == null) {
            return -1;
        }
        for (int i = 0; i < n; i++) {
            if (nodes[i] == ret) {
                return i;
            }
        }
        return "returned node is not in the original list";
    }
}
