class Solution {
    public int openLock(String[] deadends, String target) {
        Set<String> dead = new HashSet<>(Arrays.asList(deadends));
        if (dead.contains("0000")) {
            return -1;
        }
        if ("0000".equals(target)) {
            return 0;
        }

        Set<String> begin = new HashSet<>();
        Set<String> end = new HashSet<>();
        Set<String> visited = new HashSet<>();
        begin.add("0000");
        end.add(target);
        visited.add("0000");
        visited.add(target);

        int steps = 0;
        while (!begin.isEmpty() && !end.isEmpty()) {
            if (begin.size() > end.size()) {
                Set<String> tmp = begin;
                begin = end;
                end = tmp;
            }
            steps++;
            Set<String> nextFront = new HashSet<>();
            for (String code : begin) {
                char[] chars = code.toCharArray();
                for (int i = 0; i < 4; i++) {
                    char orig = chars[i];
                    int d = orig - '0';
                    int[] nextDigits = {(d + 1) % 10, (d + 9) % 10};
                    for (int nd : nextDigits) {
                        chars[i] = (char) ('0' + nd);
                        String nxt = new String(chars);
                        if (dead.contains(nxt)) continue;
                        if (end.contains(nxt)) return steps;
                        if (visited.add(nxt)) {
                            nextFront.add(nxt);
                        }
                    }
                    chars[i] = orig;
                }
            }
            begin = nextFront;
        }
        return -1;
    }
}
