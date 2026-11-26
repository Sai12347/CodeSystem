class Solution {
    public boolean isValidXml(String code) {
        int n = code.length();
        Deque<String> stack = new ArrayDeque<>();
        int i = 0;
        while (i < n) {
            if (i > 0 && stack.isEmpty()) return false;
            if (code.startsWith("<![CDATA[", i)) {
                if (stack.isEmpty()) return false;
                int end = code.indexOf("]]>", i + 9);
                if (end == -1) return false;
                i = end + 3;
            } else if (code.startsWith("</", i)) {
                int end = code.indexOf('>', i + 2);
                if (end == -1) return false;
                String tag = code.substring(i + 2, end);
                if (stack.isEmpty() || !stack.peek().equals(tag)) return false;
                stack.pop();
                i = end + 1;
            } else if (code.charAt(i) == '<') {
                int end = code.indexOf('>', i + 1);
                if (end == -1) return false;
                String tag = code.substring(i + 1, end);
                if (tag.length() < 1 || tag.length() > 9) return false;
                for (int k = 0; k < tag.length(); k++) {
                    char c = tag.charAt(k);
                    if (c < 'A' || c > 'Z') return false;
                }
                stack.push(tag);
                i = end + 1;
            } else {
                if (stack.isEmpty()) return false;
                i++;
            }
        }
        return stack.isEmpty();
    }
}
