class Solution {
    public boolean isValidSerialization(String preorder) {
        String[] tokens = preorder.split(",");
        List<String> stack = new ArrayList<>();
        for (String tok : tokens) {
            stack.add(tok);
            while (stack.size() >= 3
                    && stack.get(stack.size() - 1).equals("#")
                    && stack.get(stack.size() - 2).equals("#")
                    && !stack.get(stack.size() - 3).equals("#")) {
                stack.remove(stack.size() - 1);
                stack.remove(stack.size() - 1);
                stack.set(stack.size() - 1, "#");
            }
        }
        return stack.size() == 1 && stack.get(0).equals("#");
    }
}
