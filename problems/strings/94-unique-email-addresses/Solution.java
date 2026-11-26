class Solution {
    public int numUniqueEmails(String[] emails) {
        Set<String> seen = new HashSet<>();
        for (String e : emails) {
            int at = e.indexOf('@');
            StringBuilder sb = new StringBuilder();
            for (int i = 0; i < at; i++) {
                char c = e.charAt(i);
                if (c == '+') break;
                if (c != '.') sb.append(c);
            }
            sb.append(e, at, e.length());
            seen.add(sb.toString());
        }
        return seen.size();
    }
}
