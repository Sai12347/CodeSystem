class Solution {
    public boolean isSubPath(ListNode head, TreeNode root) {
        List<Integer> patList = new ArrayList<>();
        ListNode curr = head;
        while (curr != null) {
            patList.add(curr.val);
            curr = curr.next;
        }
        int m = patList.size();
        int[] pat = new int[m];
        for (int i = 0; i < m; i++) {
            pat[i] = patList.get(i);
        }
        int[] lps = new int[m];
        int j = 0;
        for (int i = 1; i < m; i++) {
            while (j > 0 && pat[i] != pat[j]) {
                j = lps[j - 1];
            }
            if (pat[i] == pat[j]) {
                lps[i] = ++j;
            }
        }

        Deque<TreeNode> nodeStack = new ArrayDeque<>();
        Deque<Integer> matchStack = new ArrayDeque<>();
        if (root != null) {
            nodeStack.push(root);
            matchStack.push(0);
        }
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            int k = matchStack.pop();
            while (k > 0 && node.val != pat[k]) {
                k = lps[k - 1];
            }
            if (node.val == pat[k]) {
                k++;
                if (k == m) {
                    return true;
                }
            }
            if (node.right != null) {
                nodeStack.push(node.right);
                matchStack.push(k);
            }
            if (node.left != null) {
                nodeStack.push(node.left);
                matchStack.push(k);
            }
        }
        return false;
    }
}
