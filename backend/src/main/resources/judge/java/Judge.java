import java.io.*;
import java.lang.reflect.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

/**
 * CodeSystem judge harness (Java).
 *
 * Usage: java Judge <tests.json> <results.jsonl>
 *
 * tests.json = {"signature": {...}, "tests": [{"id": "...", "input": {...}}, ...]}
 * Writes one JSON line per test to results.jsonl as soon as the test finishes:
 *   {"id": "...", "status": "OK", "output": <json>, "timeMs": 1.23, "stdout": "..."}
 *   {"id": "...", "status": "RUNTIME_ERROR", "error": "...", "timeMs": 1.23, "stdout": "..."}
 *
 * The helpers convert()/serialize() are public so that problem adapters can reuse them.
 */
public class Judge {

    private static final int MAX_STDOUT = 4096;
    private static final int MAX_LIST_NODES = 1_000_000;

    public static void main(String[] args) throws Exception {
        final String testsPath = args[0];
        final String resultsPath = args[1];
        final Throwable[] fatal = new Throwable[1];
        Thread worker = new Thread(null, () -> {
            try {
                runAll(testsPath, resultsPath);
            } catch (Throwable t) {
                fatal[0] = t;
            }
        }, "judge-main", 64L * 1024 * 1024);
        worker.start();
        worker.join();
        if (fatal[0] != null) {
            System.err.println("HARNESS_ERROR: " + fatal[0]);
            fatal[0].printStackTrace();
            System.exit(3);
        }
        System.exit(0);
    }

    @SuppressWarnings("unchecked")
    private static void runAll(String testsPath, String resultsPath) throws Exception {
        String text = new String(Files.readAllBytes(Paths.get(testsPath)), StandardCharsets.UTF_8);
        Map<String, Object> root = (Map<String, Object>) parseJson(text);
        Map<String, Object> sig = (Map<String, Object>) root.get("signature");
        List<Object> tests = (List<Object>) root.get("tests");
        PrintStream realOut = System.out;
        try (Writer w = new OutputStreamWriter(new FileOutputStream(resultsPath), StandardCharsets.UTF_8)) {
            for (Object to : tests) {
                Map<String, Object> test = (Map<String, Object>) to;
                Map<String, Object> input = (Map<String, Object>) test.get("input");
                Map<String, Object> res = new LinkedHashMap<>();
                res.put("id", test.get("id"));
                ByteArrayOutputStream captured = new ByteArrayOutputStream();
                PrintStream cap = new PrintStream(new LimitedStream(captured, MAX_STDOUT), true, "UTF-8");
                System.setOut(cap);
                long start = System.nanoTime();
                try {
                    Object out = runOne(sig, input);
                    res.put("status", "OK");
                    res.put("output", out);
                } catch (Throwable t) {
                    Throwable c = t;
                    while ((c instanceof InvocationTargetException || c instanceof ExceptionInInitializerError) && c.getCause() != null) {
                        c = c.getCause();
                    }
                    res.put("status", "RUNTIME_ERROR");
                    res.put("error", describe(c));
                } finally {
                    System.out.flush();
                    System.setOut(realOut);
                }
                double ms = (System.nanoTime() - start) / 1e6;
                res.put("timeMs", Math.round(ms * 100) / 100.0);
                res.put("stdout", new String(captured.toByteArray(), StandardCharsets.UTF_8));
                w.write(toJson(res));
                w.write("\n");
                w.flush();
            }
        }
    }

    private static String describe(Throwable t) {
        StringBuilder sb = new StringBuilder();
        sb.append(t.getClass().getName());
        if (t.getMessage() != null) sb.append(": ").append(t.getMessage());
        if (t instanceof StackOverflowError) {
            sb.append(" (recursion too deep)");
        }
        for (StackTraceElement e : t.getStackTrace()) {
            String cls = e.getClassName();
            if (!cls.startsWith("java.") && !cls.startsWith("jdk.") && !cls.startsWith("sun.") && !cls.equals("Judge")) {
                int line = e.getLineNumber();
                // Solution.java has one import line prepended to the user's code
                if ("Solution.java".equals(e.getFileName()) && line > 1) line -= 1;
                sb.append("\n    at ").append(e.getClassName()).append('.').append(e.getMethodName())
                  .append("(line ").append(line).append(')');
                break;
            }
        }
        return sb.toString();
    }

    // ------------------------------------------------------------------
    // Invocation
    // ------------------------------------------------------------------

    @SuppressWarnings("unchecked")
    private static Object runOne(Map<String, Object> sig, Map<String, Object> input) throws Throwable {
        String kind = (String) sig.getOrDefault("kind", "function");
        switch (kind) {
            case "function": return runFunction(sig, input);
            case "design": return runDesign(sig, input);
            case "adapter": {
                Class<?> ad = Class.forName("Adapter");
                Method m = ad.getDeclaredMethod("run", Map.class);
                m.setAccessible(true);
                return m.invoke(null, input);
            }
            default: throw new IllegalStateException("Unknown signature kind " + kind);
        }
    }

    @SuppressWarnings("unchecked")
    private static Object runFunction(Map<String, Object> sig, Map<String, Object> input) throws Throwable {
        String methodName = (String) sig.get("method");
        List<Object> params = (List<Object>) sig.get("params");
        String returns = (String) sig.getOrDefault("returns", "void");
        Class<?> cls = Class.forName("Solution");
        Constructor<?> ctor = cls.getDeclaredConstructor();
        ctor.setAccessible(true);
        Object inst = ctor.newInstance();
        Method m = findMethod(cls, methodName, params.size());
        Object[] callArgs = new Object[params.size()];
        String[] types = new String[params.size()];
        String[] names = new String[params.size()];
        for (int i = 0; i < params.size(); i++) {
            Map<String, Object> p = (Map<String, Object>) params.get(i);
            names[i] = (String) p.get("name");
            types[i] = (String) p.get("type");
            if (!input.containsKey(names[i])) throw new IllegalStateException("Missing input parameter " + names[i]);
            callArgs[i] = convert(input.get(names[i]), types[i]);
        }
        Object ret = m.invoke(inst, callArgs);
        Map<String, Object> output = (Map<String, Object>) sig.get("output");
        String mode = output == null ? "return" : (String) output.getOrDefault("mode", "return");
        if (mode.equals("return")) return serialize(ret, returns);
        String pname = (String) output.get("param");
        int idx = Arrays.asList(names).indexOf(pname);
        if (idx < 0) throw new IllegalStateException("Unknown output param " + pname);
        if (mode.equals("param")) return serialize(callArgs[idx], types[idx]);
        if (mode.equals("prefix")) {
            int k = ((Number) ret).intValue();
            List<Object> full = (List<Object>) serialize(callArgs[idx], types[idx]);
            if (k < 0 || k > full.size()) throw new IllegalStateException("Returned length " + k + " is out of range");
            return new ArrayList<>(full.subList(0, k));
        }
        throw new IllegalStateException("Unknown output mode " + mode);
    }

    @SuppressWarnings("unchecked")
    private static Object runDesign(Map<String, Object> sig, Map<String, Object> input) throws Throwable {
        String className = (String) sig.get("className");
        Map<String, Object> ctorSpec = (Map<String, Object>) sig.get("constructor");
        List<Object> ctorParams = ctorSpec == null ? new ArrayList<>() : (List<Object>) ctorSpec.get("params");
        Map<String, Map<String, Object>> methods = new HashMap<>();
        for (Object mo : (List<Object>) sig.get("methods")) {
            Map<String, Object> ms = (Map<String, Object>) mo;
            methods.put((String) ms.get("name"), ms);
        }
        List<Object> ops = (List<Object>) input.get("ops");
        List<Object> args = (List<Object>) input.get("args");
        if (ops == null || args == null || ops.size() != args.size()) throw new IllegalStateException("Bad design input");
        Class<?> cls = Class.forName(className);
        List<Object> out = new ArrayList<>();
        Object inst = null;
        for (int i = 0; i < ops.size(); i++) {
            String op = (String) ops.get(i);
            List<Object> a = (List<Object>) args.get(i);
            if (i == 0) {
                if (!op.equals(className)) throw new IllegalStateException("First op must be constructor " + className);
                Constructor<?> ctor = findCtor(cls, ctorParams.size());
                Object[] ca = new Object[ctorParams.size()];
                for (int j = 0; j < ca.length; j++) ca[j] = convert(a.get(j), (String) ((Map<String, Object>) ctorParams.get(j)).get("type"));
                inst = ctor.newInstance(ca);
                out.add(null);
                continue;
            }
            Map<String, Object> ms = methods.get(op);
            if (ms == null) throw new IllegalStateException("Unknown operation " + op);
            List<Object> ps = (List<Object>) ms.get("params");
            Method m = findMethod(cls, op, ps.size());
            Object[] ca = new Object[ps.size()];
            for (int j = 0; j < ca.length; j++) ca[j] = convert(a.get(j), (String) ((Map<String, Object>) ps.get(j)).get("type"));
            Object r = m.invoke(inst, ca);
            out.add(serialize(r, (String) ms.getOrDefault("returns", "void")));
        }
        return out;
    }

    private static Method findMethod(Class<?> cls, String name, int argc) throws NoSuchMethodException {
        for (Class<?> c = cls; c != null; c = c.getSuperclass()) {
            for (Method m : c.getDeclaredMethods()) {
                if (m.getName().equals(name) && m.getParameterCount() == argc && !m.isSynthetic()) {
                    m.setAccessible(true);
                    return m;
                }
            }
        }
        throw new NoSuchMethodException("Method " + name + " with " + argc + " parameter(s) not found in class " + cls.getName()
            + ". Do not rename the method from the starter code.");
    }

    private static Constructor<?> findCtor(Class<?> cls, int argc) throws NoSuchMethodException {
        for (Constructor<?> c : cls.getDeclaredConstructors()) {
            if (c.getParameterCount() == argc) {
                c.setAccessible(true);
                return c;
            }
        }
        throw new NoSuchMethodException("Constructor of " + cls.getName() + " with " + argc + " parameter(s) not found");
    }

    // ------------------------------------------------------------------
    // JSON value <-> Java typed value
    // ------------------------------------------------------------------

    public static Class<?> classOf(String type) {
        switch (type) {
            case "int": return int.class;
            case "long": return long.class;
            case "double": return double.class;
            case "boolean": return boolean.class;
            case "char": return char.class;
            case "Integer": return Integer.class;
            case "Long": return Long.class;
            case "Double": return Double.class;
            case "Boolean": return Boolean.class;
            case "Character": return Character.class;
            case "String": return String.class;
            case "ListNode": return ListNode.class;
            case "TreeNode": return TreeNode.class;
            default:
                if (type.endsWith("[]")) return Array.newInstance(classOf(type.substring(0, type.length() - 2)), 0).getClass();
                if (type.startsWith("List<")) return List.class;
                throw new IllegalArgumentException("Unsupported type " + type);
        }
    }

    @SuppressWarnings("unchecked")
    public static Object convert(Object j, String type) {
        if (type.endsWith("[]")) {
            if (j == null) return null;
            String comp = type.substring(0, type.length() - 2);
            List<Object> l = (List<Object>) j;
            Object arr = Array.newInstance(classOf(comp), l.size());
            for (int i = 0; i < l.size(); i++) Array.set(arr, i, convert(l.get(i), comp));
            return arr;
        }
        if (type.startsWith("List<")) {
            if (j == null) return null;
            String inner = type.substring(5, type.length() - 1);
            List<Object> l = (List<Object>) j;
            List<Object> res = new ArrayList<>(l.size());
            for (Object o : l) res.add(convert(o, inner));
            return res;
        }
        switch (type) {
            case "int": case "Integer": return j == null ? null : ((Number) j).intValue();
            case "long": case "Long": return j == null ? null : ((Number) j).longValue();
            case "double": case "Double": return j == null ? null : ((Number) j).doubleValue();
            case "boolean": case "Boolean": return (Boolean) j;
            case "char": case "Character": return j == null ? null : ((String) j).charAt(0);
            case "String": return (String) j;
            case "ListNode": return buildList((List<Object>) j);
            case "TreeNode": return buildTree((List<Object>) j);
            default: throw new IllegalArgumentException("Unsupported type " + type);
        }
    }

    public static Object serialize(Object v, String type) {
        if (type.equals("void")) return null;
        if (v == null) return null;
        if (type.endsWith("[]")) {
            String comp = type.substring(0, type.length() - 2);
            int n = Array.getLength(v);
            List<Object> l = new ArrayList<>(n);
            for (int i = 0; i < n; i++) l.add(serialize(Array.get(v, i), comp));
            return l;
        }
        if (type.startsWith("List<")) {
            String inner = type.substring(5, type.length() - 1);
            List<Object> l = new ArrayList<>();
            for (Object o : (Iterable<?>) v) l.add(serialize(o, inner));
            return l;
        }
        switch (type) {
            case "int": case "Integer": case "long": case "Long": return ((Number) v).longValue();
            case "double": case "Double": return ((Number) v).doubleValue();
            case "boolean": case "Boolean": return (Boolean) v;
            case "char": case "Character": return String.valueOf((char) (Character) v);
            case "String": return v.toString();
            case "ListNode": return listToJson((ListNode) v);
            case "TreeNode": return treeToJson((TreeNode) v);
            default: return generic(v);
        }
    }

    /** Best-effort serialization based on the runtime type (used for unknown declared types). */
    public static Object generic(Object v) {
        if (v == null) return null;
        if (v instanceof Integer || v instanceof Long || v instanceof Short || v instanceof Byte) return ((Number) v).longValue();
        if (v instanceof Number) return ((Number) v).doubleValue();
        if (v instanceof Boolean || v instanceof String) return v;
        if (v instanceof Character) return String.valueOf(v);
        if (v instanceof ListNode) return listToJson((ListNode) v);
        if (v instanceof TreeNode) return treeToJson((TreeNode) v);
        if (v.getClass().isArray()) {
            int n = Array.getLength(v);
            List<Object> l = new ArrayList<>(n);
            for (int i = 0; i < n; i++) l.add(generic(Array.get(v, i)));
            return l;
        }
        if (v instanceof Iterable) {
            List<Object> l = new ArrayList<>();
            for (Object o : (Iterable<?>) v) l.add(generic(o));
            return l;
        }
        if (v instanceof Map) {
            Map<String, Object> m = new LinkedHashMap<>();
            for (Map.Entry<?, ?> e : ((Map<?, ?>) v).entrySet()) m.put(String.valueOf(e.getKey()), generic(e.getValue()));
            return m;
        }
        return v.toString();
    }

    public static ListNode buildList(List<Object> vals) {
        if (vals == null) return null;
        ListNode dummy = new ListNode(0), cur = dummy;
        for (Object o : vals) {
            cur.next = new ListNode(((Number) o).intValue());
            cur = cur.next;
        }
        return dummy.next;
    }

    public static List<Object> listToJson(ListNode head) {
        List<Object> l = new ArrayList<>();
        int count = 0;
        for (ListNode c = head; c != null; c = c.next) {
            if (++count > MAX_LIST_NODES) throw new IllegalStateException("Returned linked list is too long or contains a cycle");
            l.add((long) c.val);
        }
        return l;
    }

    public static TreeNode buildTree(List<Object> vals) {
        if (vals == null || vals.isEmpty() || vals.get(0) == null) return null;
        TreeNode root = new TreeNode(((Number) vals.get(0)).intValue());
        ArrayDeque<TreeNode> q = new ArrayDeque<>();
        q.add(root);
        int i = 1;
        while (!q.isEmpty() && i < vals.size()) {
            TreeNode n = q.poll();
            if (i < vals.size()) {
                Object o = vals.get(i++);
                if (o != null) { n.left = new TreeNode(((Number) o).intValue()); q.add(n.left); }
            }
            if (i < vals.size()) {
                Object o = vals.get(i++);
                if (o != null) { n.right = new TreeNode(((Number) o).intValue()); q.add(n.right); }
            }
        }
        return root;
    }

    public static List<Object> treeToJson(TreeNode root) {
        List<Object> l = new ArrayList<>();
        if (root == null) return l;
        int count = 0;
        // LinkedList (not ArrayDeque) because the queue must hold null children
        LinkedList<TreeNode> queue = new LinkedList<>();
        queue.add(root);
        while (!queue.isEmpty()) {
            TreeNode n = queue.poll();
            if (++count > 4 * MAX_LIST_NODES) throw new IllegalStateException("Returned tree is too large or contains a cycle");
            if (n == null) { l.add(null); continue; }
            l.add((long) n.val);
            queue.add(n.left);
            queue.add(n.right);
        }
        while (!l.isEmpty() && l.get(l.size() - 1) == null) l.remove(l.size() - 1);
        return l;
    }

    // ------------------------------------------------------------------
    // Minimal JSON parser / writer
    // ------------------------------------------------------------------

    public static Object parseJson(String s) {
        int[] pos = {0};
        Object v = parseValue(s, pos);
        skipWs(s, pos);
        if (pos[0] != s.length()) throw new IllegalArgumentException("Trailing data in JSON at " + pos[0]);
        return v;
    }

    private static void skipWs(String s, int[] p) {
        while (p[0] < s.length() && Character.isWhitespace(s.charAt(p[0]))) p[0]++;
    }

    private static Object parseValue(String s, int[] p) {
        skipWs(s, p);
        char c = s.charAt(p[0]);
        if (c == '{') {
            p[0]++;
            Map<String, Object> m = new LinkedHashMap<>();
            skipWs(s, p);
            if (s.charAt(p[0]) == '}') { p[0]++; return m; }
            while (true) {
                skipWs(s, p);
                String k = parseString(s, p);
                skipWs(s, p);
                if (s.charAt(p[0]) != ':') throw new IllegalArgumentException("Expected : at " + p[0]);
                p[0]++;
                m.put(k, parseValue(s, p));
                skipWs(s, p);
                char d = s.charAt(p[0]++);
                if (d == '}') return m;
                if (d != ',') throw new IllegalArgumentException("Expected , or } at " + (p[0] - 1));
            }
        }
        if (c == '[') {
            p[0]++;
            List<Object> l = new ArrayList<>();
            skipWs(s, p);
            if (s.charAt(p[0]) == ']') { p[0]++; return l; }
            while (true) {
                l.add(parseValue(s, p));
                skipWs(s, p);
                char d = s.charAt(p[0]++);
                if (d == ']') return l;
                if (d != ',') throw new IllegalArgumentException("Expected , or ] at " + (p[0] - 1));
            }
        }
        if (c == '"') return parseString(s, p);
        if (s.startsWith("true", p[0])) { p[0] += 4; return Boolean.TRUE; }
        if (s.startsWith("false", p[0])) { p[0] += 5; return Boolean.FALSE; }
        if (s.startsWith("null", p[0])) { p[0] += 4; return null; }
        int start = p[0];
        while (p[0] < s.length() && "+-0123456789.eE".indexOf(s.charAt(p[0])) >= 0) p[0]++;
        String num = s.substring(start, p[0]);
        if (num.isEmpty()) throw new IllegalArgumentException("Unexpected character '" + c + "' at " + start);
        if (num.contains(".") || num.contains("e") || num.contains("E")) return Double.parseDouble(num);
        try {
            return Long.parseLong(num);
        } catch (NumberFormatException e) {
            return Double.parseDouble(num);
        }
    }

    private static String parseString(String s, int[] p) {
        if (s.charAt(p[0]) != '"') throw new IllegalArgumentException("Expected string at " + p[0]);
        p[0]++;
        StringBuilder sb = new StringBuilder();
        while (true) {
            char c = s.charAt(p[0]++);
            if (c == '"') return sb.toString();
            if (c == '\\') {
                char e = s.charAt(p[0]++);
                switch (e) {
                    case '"': sb.append('"'); break;
                    case '\\': sb.append('\\'); break;
                    case '/': sb.append('/'); break;
                    case 'b': sb.append('\b'); break;
                    case 'f': sb.append('\f'); break;
                    case 'n': sb.append('\n'); break;
                    case 'r': sb.append('\r'); break;
                    case 't': sb.append('\t'); break;
                    case 'u': sb.append((char) Integer.parseInt(s.substring(p[0], p[0] + 4), 16)); p[0] += 4; break;
                    default: throw new IllegalArgumentException("Bad escape at " + p[0]);
                }
            } else {
                sb.append(c);
            }
        }
    }

    public static String toJson(Object v) {
        StringBuilder sb = new StringBuilder();
        writeJson(v, sb);
        return sb.toString();
    }

    @SuppressWarnings("unchecked")
    private static void writeJson(Object v, StringBuilder sb) {
        if (v == null) { sb.append("null"); return; }
        if (v instanceof String) { writeString((String) v, sb); return; }
        if (v instanceof Boolean) { sb.append(v); return; }
        if (v instanceof Double || v instanceof Float) {
            double d = ((Number) v).doubleValue();
            if (Double.isNaN(d) || Double.isInfinite(d)) { writeString(Double.toString(d), sb); return; }
            sb.append(Double.toString(d));
            return;
        }
        if (v instanceof Number) { sb.append(((Number) v).longValue()); return; }
        if (v instanceof Map) {
            sb.append('{');
            boolean first = true;
            for (Map.Entry<String, Object> e : ((Map<String, Object>) v).entrySet()) {
                if (!first) sb.append(',');
                first = false;
                writeString(e.getKey(), sb);
                sb.append(':');
                writeJson(e.getValue(), sb);
            }
            sb.append('}');
            return;
        }
        if (v instanceof List) {
            sb.append('[');
            boolean first = true;
            for (Object o : (List<Object>) v) {
                if (!first) sb.append(',');
                first = false;
                writeJson(o, sb);
            }
            sb.append(']');
            return;
        }
        writeJson(generic(v), sb);
    }

    private static void writeString(String s, StringBuilder sb) {
        sb.append('"');
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            switch (c) {
                case '"': sb.append("\\\""); break;
                case '\\': sb.append("\\\\"); break;
                case '\n': sb.append("\\n"); break;
                case '\r': sb.append("\\r"); break;
                case '\t': sb.append("\\t"); break;
                default:
                    if (c < 0x20) sb.append(String.format("\\u%04x", (int) c));
                    else sb.append(c);
            }
        }
        sb.append('"');
    }

    /** Output stream that silently drops bytes beyond a limit. */
    private static final class LimitedStream extends OutputStream {
        private final OutputStream inner;
        private final int limit;
        private int written;
        LimitedStream(OutputStream inner, int limit) { this.inner = inner; this.limit = limit; }
        @Override public void write(int b) throws IOException {
            if (written < limit) { inner.write(b); written++; }
        }
        @Override public void write(byte[] b, int off, int len) throws IOException {
            int n = Math.min(len, limit - written);
            if (n > 0) { inner.write(b, off, n); written += n; }
        }
    }
}
