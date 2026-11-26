class Solution {
    public String countOfAtoms(String formula) {
        Deque<Map<String, Integer>> stack = new ArrayDeque<>();
        stack.push(new HashMap<>());
        int i = 0, n = formula.length();
        while (i < n) {
            char ch = formula.charAt(i);
            if (ch == '(') {
                stack.push(new HashMap<>());
                i++;
            } else if (ch == ')') {
                i++;
                int mult = 0;
                while (i < n && Character.isDigit(formula.charAt(i))) {
                    mult = mult * 10 + (formula.charAt(i) - '0');
                    i++;
                }
                if (mult == 0) mult = 1;
                Map<String, Integer> top = stack.pop();
                Map<String, Integer> cur = stack.peek();
                for (Map.Entry<String, Integer> e : top.entrySet()) {
                    cur.put(e.getKey(), cur.getOrDefault(e.getKey(), 0) + e.getValue() * mult);
                }
            } else {
                int j = i + 1;
                while (j < n && Character.isLowerCase(formula.charAt(j))) j++;
                String atom = formula.substring(i, j);
                i = j;
                int cnt = 0;
                while (i < n && Character.isDigit(formula.charAt(i))) {
                    cnt = cnt * 10 + (formula.charAt(i) - '0');
                    i++;
                }
                if (cnt == 0) cnt = 1;
                Map<String, Integer> cur = stack.peek();
                cur.put(atom, cur.getOrDefault(atom, 0) + cnt);
            }
        }
        TreeMap<String, Integer> sorted = new TreeMap<>(stack.peek());
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, Integer> e : sorted.entrySet()) {
            sb.append(e.getKey());
            if (e.getValue() > 1) sb.append(e.getValue());
        }
        return sb.toString();
    }
}
