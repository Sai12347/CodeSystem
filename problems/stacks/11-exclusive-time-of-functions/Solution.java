class Solution {
    public int[] exclusiveTime(int n, List<String> logs) {
        int[] res = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        int prev = 0;
        for (String entry : logs) {
            int c1 = entry.indexOf(':');
            int c2 = entry.lastIndexOf(':');
            int fid = Integer.parseInt(entry.substring(0, c1));
            int ts = Integer.parseInt(entry.substring(c2 + 1));
            if (entry.charAt(c1 + 1) == 's') {
                if (!stack.isEmpty()) {
                    res[stack.peek()] += ts - prev;
                }
                stack.push(fid);
                prev = ts;
            } else {
                res[stack.pop()] += ts - prev + 1;
                prev = ts + 1;
            }
        }
        return res;
    }
}
