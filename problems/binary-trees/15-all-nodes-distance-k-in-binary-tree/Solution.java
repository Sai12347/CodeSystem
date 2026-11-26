class Solution {
    public List<Integer> distanceK(TreeNode root, TreeNode target, int k) {
        List<Integer> result = new ArrayList<>();
        if (root == null || target == null) {
            return result;
        }
        Map<TreeNode, TreeNode> parent = new HashMap<>();
        ArrayDeque<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (node.left != null) {
                parent.put(node.left, node);
                q.add(node.left);
            }
            if (node.right != null) {
                parent.put(node.right, node);
                q.add(node.right);
            }
        }

        ArrayDeque<TreeNode> bfs = new ArrayDeque<>();
        Set<TreeNode> visited = new HashSet<>();
        bfs.add(target);
        visited.add(target);
        int dist = 0;

        while (!bfs.isEmpty() && dist < k) {
            int size = bfs.size();
            for (int i = 0; i < size; i++) {
                TreeNode curr = bfs.poll();
                TreeNode[] neighbors = {curr.left, curr.right, parent.get(curr)};
                for (TreeNode nxt : neighbors) {
                    if (nxt != null && visited.add(nxt)) {
                        bfs.add(nxt);
                    }
                }
            }
            dist++;
        }

        while (!bfs.isEmpty()) {
            result.add(bfs.poll().val);
        }
        return result;
    }
}
