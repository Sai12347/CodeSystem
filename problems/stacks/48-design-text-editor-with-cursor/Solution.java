class TextEditor {
    private final StringBuilder left = new StringBuilder();
    private final StringBuilder right = new StringBuilder();

    public TextEditor() {}

    public void addText(String text) {
        left.append(text);
    }

    public int deleteText(int k) {
        int cnt = Math.min(k, left.length());
        left.setLength(left.length() - cnt);
        return cnt;
    }

    public String cursorLeft(int k) {
        int moves = Math.min(k, left.length());
        for (int i = 0; i < moves; i++) {
            int last = left.length() - 1;
            right.append(left.charAt(last));
            left.setLength(last);
        }
        return leftTail();
    }

    public String cursorRight(int k) {
        int moves = Math.min(k, right.length());
        for (int i = 0; i < moves; i++) {
            int last = right.length() - 1;
            left.append(right.charAt(last));
            right.setLength(last);
        }
        return leftTail();
    }

    private String leftTail() {
        int start = Math.max(0, left.length() - 10);
        return left.substring(start);
    }
}
