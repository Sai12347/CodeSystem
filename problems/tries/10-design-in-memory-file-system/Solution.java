class FileSystem {
    private static class Node {
        TreeMap<String, Node> children = new TreeMap<>();
        boolean isFile;
        StringBuilder content = new StringBuilder();
    }

    private final Node root;

    public FileSystem() {
        root = new Node();
    }

    private Node traverse(String path, boolean create) {
        Node cur = root;
        if (path.equals("/")) {
            return cur;
        }
        String[] parts = path.split("/");
        for (int i = 1; i < parts.length; i++) {
            String part = parts[i];
            Node next = cur.children.get(part);
            if (next == null) {
                if (!create) {
                    throw new IllegalArgumentException("Path not found: " + path);
                }
                next = new Node();
                cur.children.put(part, next);
            }
            cur = next;
        }
        return cur;
    }

    public List<String> ls(String path) {
        Node node = traverse(path, false);
        if (node.isFile) {
            int idx = path.lastIndexOf('/');
            return Collections.singletonList(path.substring(idx + 1));
        }
        return new ArrayList<>(node.children.keySet());
    }

    public void mkdir(String path) {
        traverse(path, true);
    }

    public void addContentToFile(String filePath, String content) {
        Node node = traverse(filePath, true);
        node.isFile = true;
        node.content.append(content);
    }

    public String readContentFromFile(String filePath) {
        Node node = traverse(filePath, false);
        return node.content.toString();
    }
}
