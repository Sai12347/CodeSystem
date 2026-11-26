class Solution {
    public List<String> braceExpansion(String expression) {
        Deque<Set<String>> unionSt = new ArrayDeque<>();
        Deque<Set<String>> curSt = new ArrayDeque<>();
        Set<String> unionSet = new HashSet<>();
        Set<String> curSet = new HashSet<>();
        curSet.add("");
        for (int i = 0; i < expression.length(); i++) {
            char ch = expression.charAt(i);
            if (ch == '{') {
                unionSt.push(unionSet);
                curSt.push(curSet);
                unionSet = new HashSet<>();
                curSet = new HashSet<>();
                curSet.add("");
            } else if (ch == ',') {
                unionSet.addAll(curSet);
                curSet = new HashSet<>();
                curSet.add("");
            } else if (ch == '}') {
                unionSet.addAll(curSet);
                Set<String> prevUnion = unionSt.pop();
                Set<String> prevCur = curSt.pop();
                Set<String> nextCur = new HashSet<>();
                for (String a : prevCur) {
                    for (String b : unionSet) {
                        nextCur.add(a + b);
                    }
                }
                curSet = nextCur;
                unionSet = prevUnion;
            } else {
                Set<String> nextCur = new HashSet<>();
                for (String a : curSet) {
                    nextCur.add(a + ch);
                }
                curSet = nextCur;
            }
        }
        unionSet.addAll(curSet);
        List<String> ans = new ArrayList<>(unionSet);
        Collections.sort(ans);
        return ans;
    }
}
