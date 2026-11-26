class Solution {
    public String simplifyPath(String path) {
        List<String> stack = new ArrayList<>();
        for (String part : path.split("/")) {
            if (part.isEmpty() || part.equals(".")) {
                continue;
            }
            if (part.equals("..")) {
                if (!stack.isEmpty()) {
                    stack.remove(stack.size() - 1);
                }
            } else {
                stack.add(part);
            }
        }
        return "/" + String.join("/", stack);
    }
}
