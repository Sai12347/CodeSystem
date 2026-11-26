class Solution {
    public long peakStackMemory(String[] events) {
        Deque<Long> stack = new ArrayDeque<>();
        long cur = 0L, peak = 0L;
        for (String ev : events) {
            if (ev.equals("RET")) {
                cur -= stack.pop();
            } else if (ev.charAt(0) == 'C') {
                long val = Long.parseLong(ev.substring(5));
                stack.push(val);
                cur += val;
                if (cur > peak) peak = cur;
            } else if (ev.charAt(0) == 'A') {
                long val = Long.parseLong(ev.substring(6));
                long top = stack.pop() + val;
                stack.push(top);
                cur += val;
                if (cur > peak) peak = cur;
            } else {
                long val = Long.parseLong(ev.substring(7));
                long top = stack.pop();
                long freed = Math.min(top, val);
                stack.push(top - freed);
                cur -= freed;
            }
        }
        return peak;
    }
}
