class Adapter {
    private static boolean verifyIntact(ListNode head, ListNode[] expectedNodes, List<Object> expectedVals) {
        ListNode cur = head;
        for (int i = 0; i < expectedNodes.length; i++) {
            if (cur != expectedNodes[i] || cur.val != ((Number) expectedVals.get(i)).intValue()) {
                return false;
            }
            cur = cur.next;
        }
        return cur == null;
    }

    @SuppressWarnings("unchecked")
    public static Object run(Map<String, Object> inp) {
        List<Object> listA = (List<Object>) inp.get("listA");
        List<Object> listB = (List<Object>) inp.get("listB");
        int skipA = ((Number) inp.get("skipA")).intValue();
        int skipB = ((Number) inp.get("skipB")).intValue();

        int sharedLen = (skipA < listA.size() && skipB < listB.size()) ? (listA.size() - skipA) : 0;
        ListNode[] shared = new ListNode[sharedLen];
        for (int i = 0; i < sharedLen; i++) {
            shared[i] = new ListNode(((Number) listA.get(skipA + i)).intValue());
        }

        ListNode[] nodesA = new ListNode[skipA + sharedLen];
        for (int i = 0; i < skipA; i++) {
            nodesA[i] = new ListNode(((Number) listA.get(i)).intValue());
        }
        for (int i = 0; i < sharedLen; i++) {
            nodesA[skipA + i] = shared[i];
        }
        for (int i = 0; i < nodesA.length - 1; i++) {
            nodesA[i].next = nodesA[i + 1];
        }

        ListNode[] nodesB = new ListNode[skipB + sharedLen];
        for (int i = 0; i < skipB; i++) {
            nodesB[i] = new ListNode(((Number) listB.get(i)).intValue());
        }
        for (int i = 0; i < sharedLen; i++) {
            nodesB[skipB + i] = shared[i];
        }
        for (int i = 0; i < nodesB.length - 1; i++) {
            nodesB[i].next = nodesB[i + 1];
        }

        ListNode headA = nodesA.length > 0 ? nodesA[0] : null;
        ListNode headB = nodesB.length > 0 ? nodesB[0] : null;
        ListNode expectedNode = sharedLen > 0 ? shared[0] : null;

        ListNode ans = new Solution().getIntersectionNode(headA, headB);

        if (!verifyIntact(headA, nodesA, listA) || !verifyIntact(headB, nodesB, listB)) {
            return "ERROR: input linked lists were modified";
        }
        if (ans == null) {
            return null;
        }
        if (ans != expectedNode) {
            return "ERROR: returned wrong node reference (val=" + ans.val + ")";
        }
        return (long) ans.val;
    }
}
