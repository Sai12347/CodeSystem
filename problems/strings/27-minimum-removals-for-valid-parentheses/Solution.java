class Solution {
    public String minRemoveToMakeValid(String s) {
        StringBuilder kept = new StringBuilder(); int open = 0;
        for (int i = 0; i < s.length(); i++) { char c = s.charAt(i); if (c == '(') { open++; kept.append(c); } else if (c == ')') { if (open == 0) continue; open--; kept.append(c); } else kept.append(c); }
        StringBuilder out = new StringBuilder();
        for (int i = kept.length() - 1; i >= 0; i--) { char c = kept.charAt(i); if (c == '(' && open > 0) open--; else out.append(c); }
        return out.reverse().toString();
    }
}
