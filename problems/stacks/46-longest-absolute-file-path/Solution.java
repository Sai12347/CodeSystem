class Solution {
    public int lengthLongestPath(String input) {
        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(0);
        int best = 0;
        String[] lines = input.split("\n");
        for (String line : lines) {
            int depth = 0;
            while (depth < line.length() && line.charAt(depth) == '\t') {
                depth++;
            }
            String name = line.substring(depth);
            while (stack.size() > depth + 1) {
                stack.pop();
            }
            int curLen = stack.peek() + name.length();
            if (name.indexOf('.') >= 0) {
                if (curLen > best) best = curLen;
            } else {
                stack.push(curLen + 1);
            }
        }
        return best;
    }
}
