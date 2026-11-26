class Solution {
    public int evaluateExpression(String s) {
        Deque<List<Integer>> frameTerms = new ArrayDeque<>();
        Deque<Character> frameOps = new ArrayDeque<>();
        List<Integer> terms = new ArrayList<>();
        char op = '+';
        int num = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ' ') continue;
            if (ch >= '0' && ch <= '9') {
                num = num * 10 + (ch - '0');
            } else if (ch == '(') {
                frameTerms.push(terms);
                frameOps.push(op);
                terms = new ArrayList<>();
                op = '+';
                num = 0;
            } else if (ch == ')') {
                if (op == '+') terms.add(num);
                else if (op == '-') terms.add(-num);
                else if (op == '*') terms.set(terms.size() - 1, terms.get(terms.size() - 1) * num);
                else terms.set(terms.size() - 1, terms.get(terms.size() - 1) / num);
                int val = 0;
                for (int t : terms) val += t;
                terms = frameTerms.pop();
                op = frameOps.pop();
                num = val;
            } else {
                if (op == '+') terms.add(num);
                else if (op == '-') terms.add(-num);
                else if (op == '*') terms.set(terms.size() - 1, terms.get(terms.size() - 1) * num);
                else terms.set(terms.size() - 1, terms.get(terms.size() - 1) / num);
                op = ch;
                num = 0;
            }
        }
        if (op == '+') terms.add(num);
        else if (op == '-') terms.add(-num);
        else if (op == '*') terms.set(terms.size() - 1, terms.get(terms.size() - 1) * num);
        else terms.set(terms.size() - 1, terms.get(terms.size() - 1) / num);
        int ans = 0;
        for (int t : terms) ans += t;
        return ans;
    }
}
