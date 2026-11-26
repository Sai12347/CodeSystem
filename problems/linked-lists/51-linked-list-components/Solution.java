class Solution {
    public int numComponents(ListNode head, int[] nums) {
        Set<Integer> present = new HashSet<>();
        for (int x : nums) {
            present.add(x);
        }
        int ans = 0;
        ListNode curr = head;
        while (curr != null) {
            if (present.contains(curr.val) && (curr.next == null || !present.contains(curr.next.val))) {
                ans++;
            }
            curr = curr.next;
        }
        return ans;
    }
}
