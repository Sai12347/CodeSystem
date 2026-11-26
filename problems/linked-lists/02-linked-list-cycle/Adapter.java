class Adapter {
    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> vals = (List<Object>) inp.get("head");
        int pos = ((Number) inp.get("pos")).intValue();
        ListNode[] nodes = new ListNode[vals.size()];
        for (int i = 0; i < vals.size(); i++) {
            nodes[i] = new ListNode(((Number) vals.get(i)).intValue());
        }
        for (int i = 0; i < nodes.length - 1; i++) {
            nodes[i].next = nodes[i + 1];
        }
        if (nodes.length > 0 && pos >= 0) {
            nodes[nodes.length - 1].next = nodes[pos];
        }
        ListNode head = nodes.length > 0 ? nodes[0] : null;
        return new Solution().hasCycle(head);
    }
}
