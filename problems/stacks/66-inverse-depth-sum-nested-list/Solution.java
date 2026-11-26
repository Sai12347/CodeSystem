class Solution {
    public int inverseDepthSum(String s) {
        Deque<Character> stack = new ArrayDeque<>();
        int plainSum = 0;
        int depthSum = 0;
        int maxDepth = 0;
        int i = 0, n = s.length();
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == '[') {
                stack.push(ch);
                i++;
            } else if (ch == ']') {
                stack.pop();
                i++;
            } else if (ch == ',') {
                i++;
            } else {
                int sign = 1;
                if (ch == '-') {
                    sign = -1;
                    i++;
                }
                int val = 0;
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    val = val * 10 + (s.charAt(i) - '0');
                    i++;
                }
                val *= sign;
                int d = stack.size();
                if (d > maxDepth) maxDepth = d;
                plainSum += val;
                depthSum += val * d;
            }
        }
        return (maxDepth + 1) * plainSum - depthSum;
    }
}
