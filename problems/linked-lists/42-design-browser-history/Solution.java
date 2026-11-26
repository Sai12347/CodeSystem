class BrowserHistory {
    private static class Node {
        final String url;
        Node prev;
        Node next;

        Node(String url) {
            this.url = url;
        }
    }

    private Node curr;

    public BrowserHistory(String homepage) {
        this.curr = new Node(homepage);
    }

    public void visit(String url) {
        Node node = new Node(url);
        node.prev = curr;
        curr.next = node;
        curr = node;
    }

    public String back(int steps) {
        while (steps > 0 && curr.prev != null) {
            curr = curr.prev;
            steps--;
        }
        return curr.url;
    }

    public String forward(int steps) {
        while (steps > 0 && curr.next != null) {
            curr = curr.next;
            steps--;
        }
        return curr.url;
    }
}
