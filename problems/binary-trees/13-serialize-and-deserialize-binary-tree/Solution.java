class Codec {
    public String serialize(TreeNode root) {
        if (root == null) {
            return "";
        }
        StringBuilder sb = new StringBuilder();
        LinkedList<TreeNode> q = new LinkedList<>();
        q.add(root);
        while (!q.isEmpty()) {
            TreeNode node = q.poll();
            if (sb.length() > 0) {
                sb.append(',');
            }
            if (node == null) {
                sb.append('#');
            } else {
                sb.append(node.val);
                q.add(node.left);
                q.add(node.right);
            }
        }
        return sb.toString();
    }

    public TreeNode deserialize(String data) {
        if (data == null || data.isEmpty()) {
            return null;
        }
        String[] tokens = data.split(",");
        TreeNode root = new TreeNode(Integer.parseInt(tokens[0]));
        ArrayDeque<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty() && i < tokens.length) {
            TreeNode node = q.poll();
            if (!tokens[i].equals("#")) {
                node.left = new TreeNode(Integer.parseInt(tokens[i]));
                q.add(node.left);
            }
            i++;
            if (i < tokens.length && !tokens[i].equals("#")) {
                node.right = new TreeNode(Integer.parseInt(tokens[i]));
                q.add(node.right);
            }
            i++;
        }
        return root;
    }
}
