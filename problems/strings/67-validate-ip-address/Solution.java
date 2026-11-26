class Solution {
    public String validIPAddress(String queryIP) {
        if (queryIP.indexOf('.') >= 0) {
            String[] parts = queryIP.split("\\.", -1);
            if (parts.length != 4) return "Neither";
            for (String p : parts) {
                if (p.isEmpty() || p.length() > 3) return "Neither";
                if (p.length() > 1 && p.charAt(0) == '0') return "Neither";
                int val = 0;
                for (int i = 0; i < p.length(); i++) {
                    char c = p.charAt(i);
                    if (c < '0' || c > '9') return "Neither";
                    val = val * 10 + (c - '0');
                }
                if (val > 255) return "Neither";
            }
            return "IPv4";
        }
        if (queryIP.indexOf(':') >= 0) {
            String[] parts = queryIP.split(":", -1);
            if (parts.length != 8) return "Neither";
            for (String p : parts) {
                if (p.isEmpty() || p.length() > 4) return "Neither";
                for (int i = 0; i < p.length(); i++) {
                    char c = p.charAt(i);
                    boolean ok = (c >= '0' && c <= '9') || (c >= 'a' && c <= 'f') || (c >= 'A' && c <= 'F');
                    if (!ok) return "Neither";
                }
            }
            return "IPv6";
        }
        return "Neither";
    }
}
