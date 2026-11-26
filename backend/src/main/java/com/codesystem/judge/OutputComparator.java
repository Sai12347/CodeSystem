package com.codesystem.judge;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.DoubleNode;
import com.fasterxml.jackson.databind.node.LongNode;
import com.fasterxml.jackson.databind.node.ObjectNode;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.Iterator;
import java.util.List;
import java.util.Map;
import java.util.TreeMap;

/**
 * Compares judge outputs against expected JSON values using the same modes as tools/problems/judgekit.py:
 * exact, float (1e-5 tolerance), sorted, sortedDeep, and anyOf.
 */
public final class OutputComparator {

    private static final double FLOAT_TOL = 1e-5;
    private static final ObjectMapper MAPPER = new ObjectMapper();

    private OutputComparator() {}

    public static boolean compare(JsonNode expected, JsonNode actual, String mode) {
        String effectiveMode = (mode == null || mode.isBlank()) ? "exact" : mode;
        return switch (effectiveMode) {
            case "exact" -> valuesEqual(normalize(expected), normalize(actual), null);
            case "float" -> valuesEqual(expected, actual, FLOAT_TOL);
            case "sorted" -> {
                if (expected == null || actual == null || !expected.isArray() || !actual.isArray()) {
                    yield valuesEqual(normalize(expected), normalize(actual), null);
                }
                yield valuesEqual(sortTopLevel(normalize(expected)), sortTopLevel(normalize(actual)), null);
            }
            case "sortedDeep" -> valuesEqual(deepSort(normalize(expected)), deepSort(normalize(actual)), null);
            case "anyOf" -> {
                if (expected == null || !expected.isArray()) {
                    yield false;
                }
                JsonNode normActual = normalize(actual);
                boolean matched = false;
                for (JsonNode option : expected) {
                    if (valuesEqual(normalize(option), normActual, null)) {
                        matched = true;
                        break;
                    }
                }
                yield matched;
            }
            default -> throw new IllegalArgumentException("Unknown compare mode: " + effectiveMode);
        };
    }

    static JsonNode normalize(JsonNode node) {
        if (node == null || node.isNull() || node.isBoolean() || node.isTextual()) {
            return node;
        }
        if (node.isIntegralNumber()) {
            return LongNode.valueOf(node.longValue());
        }
        if (node.isFloatingPointNumber()) {
            double d = node.doubleValue();
            if (Double.isFinite(d) && d == Math.rint(d) && Math.abs(d) < 9007199254740992.0) {
                return LongNode.valueOf((long) d);
            }
            return DoubleNode.valueOf(d);
        }
        if (node.isArray()) {
            ArrayNode arr = MAPPER.createArrayNode();
            for (JsonNode item : node) {
                arr.add(normalize(item));
            }
            return arr;
        }
        if (node.isObject()) {
            ObjectNode obj = MAPPER.createObjectNode();
            TreeMap<String, JsonNode> sorted = new TreeMap<>();
            Iterator<Map.Entry<String, JsonNode>> it = node.fields();
            while (it.hasNext()) {
                Map.Entry<String, JsonNode> e = it.next();
                sorted.put(e.getKey(), normalize(e.getValue()));
            }
            sorted.forEach(obj::set);
            return obj;
        }
        return node;
    }

    static String canonical(JsonNode node) {
        try {
            return MAPPER.writeValueAsString(normalize(node));
        } catch (Exception e) {
            return String.valueOf(node);
        }
    }

    private static JsonNode sortTopLevel(JsonNode node) {
        if (!node.isArray()) {
            return node;
        }
        List<JsonNode> items = new ArrayList<>();
        node.forEach(items::add);
        items.sort(Comparator.comparing(OutputComparator::canonical));
        ArrayNode arr = MAPPER.createArrayNode();
        items.forEach(arr::add);
        return arr;
    }

    private static JsonNode deepSort(JsonNode node) {
        if (node == null || !node.isArray()) {
            return node;
        }
        List<JsonNode> items = new ArrayList<>();
        for (JsonNode item : node) {
            items.add(deepSort(item));
        }
        items.sort(Comparator.comparing(OutputComparator::canonical));
        ArrayNode arr = MAPPER.createArrayNode();
        items.forEach(arr::add);
        return arr;
    }

    private static boolean valuesEqual(JsonNode a, JsonNode b, Double tol) {
        if (a == b) return true;
        if (a == null || b == null) return false;
        if (a.isNull() && b.isNull()) return true;
        if (a.isBoolean() || b.isBoolean()) {
            return a.isBoolean() && b.isBoolean() && a.booleanValue() == b.booleanValue();
        }
        if (a.isNumber() && b.isNumber()) {
            if (tol == null) {
                JsonNode na = normalize(a);
                JsonNode nb = normalize(b);
                if (na.isIntegralNumber() && nb.isIntegralNumber()) {
                    return na.longValue() == nb.longValue();
                }
                return Double.compare(na.doubleValue(), nb.doubleValue()) == 0;
            }
            double da = a.doubleValue();
            double db = b.doubleValue();
            double diff = Math.abs(da - db);
            return diff <= tol || diff <= tol * Math.max(Math.abs(da), Math.abs(db));
        }
        if (a.isTextual() && b.isTextual()) {
            return a.textValue().equals(b.textValue());
        }
        if (a.isArray() && b.isArray()) {
            if (a.size() != b.size()) return false;
            for (int i = 0; i < a.size(); i++) {
                if (!valuesEqual(a.get(i), b.get(i), tol)) return false;
            }
            return true;
        }
        if (a.isObject() && b.isObject()) {
            if (a.size() != b.size()) return false;
            Iterator<Map.Entry<String, JsonNode>> it = a.fields();
            while (it.hasNext()) {
                Map.Entry<String, JsonNode> e = it.next();
                if (!b.has(e.getKey()) || !valuesEqual(e.getValue(), b.get(e.getKey()), tol)) {
                    return false;
                }
            }
            return true;
        }
        return false;
    }
}
