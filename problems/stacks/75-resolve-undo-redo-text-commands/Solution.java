class Solution {
    public String applyUndoRedo(String[] commands) {
        Deque<String> undo = new ArrayDeque<>();
        Deque<String> redo = new ArrayDeque<>();
        for (String cmd : commands) {
            if (cmd.equals("UNDO")) {
                if (!undo.isEmpty()) redo.push(undo.pop());
            } else if (cmd.equals("REDO")) {
                if (!redo.isEmpty()) undo.push(redo.pop());
            } else {
                undo.push(cmd.substring(5));
                redo.clear();
            }
        }
        StringBuilder sb = new StringBuilder();
        Iterator<String> it = undo.descendingIterator();
        while (it.hasNext()) {
            sb.append(it.next());
        }
        return sb.toString();
    }
}
