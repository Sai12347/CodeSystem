class Solution {
    public String makeLargestSpecial(String s) {
        Deque<List<String>> frames = new ArrayDeque<>();
        frames.push(new ArrayList<>());
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '1') {
                frames.push(new ArrayList<>());
            } else {
                List<String> inner = frames.pop();
                inner.sort(Collections.reverseOrder());
                StringBuilder sb = new StringBuilder("1");
                for (String part : inner) sb.append(part);
                sb.append('0');
                frames.peek().add(sb.toString());
            }
        }
        List<String> top = frames.pop();
        top.sort(Collections.reverseOrder());
        StringBuilder ans = new StringBuilder();
        for (String part : top) ans.append(part);
        return ans.toString();
    }
}
