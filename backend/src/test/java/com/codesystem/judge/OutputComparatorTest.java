package com.codesystem.judge;

import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class OutputComparatorTest {

    private final ObjectMapper mapper = new ObjectMapper();

    @Test
    void exactComparisonNormalizesIntegersAndFloats() throws Exception {
        assertTrue(OutputComparator.compare(mapper.readTree("[1, 2, 3]"), mapper.readTree("[1, 2.0, 3]"), "exact"));
        assertFalse(OutputComparator.compare(mapper.readTree("[1, 2]"), mapper.readTree("[2, 1]"), "exact"));
        assertFalse(OutputComparator.compare(mapper.readTree("true"), mapper.readTree("1"), "exact"));
    }

    @Test
    void floatComparisonRespectsTolerance() throws Exception {
        assertTrue(OutputComparator.compare(mapper.readTree("2.5"), mapper.readTree("2.500001"), "float"));
        assertFalse(OutputComparator.compare(mapper.readTree("2.5"), mapper.readTree("2.501"), "float"));
    }

    @Test
    void sortedAndSortedDeepComparison() throws Exception {
        assertTrue(OutputComparator.compare(mapper.readTree("[1, 2, 3]"), mapper.readTree("[3, 1, 2]"), "sorted"));
        assertTrue(OutputComparator.compare(
                mapper.readTree("[[-1, 0, 1], [-1, -1, 2]]"),
                mapper.readTree("[[2, -1, -1], [1, 0, -1]]"),
                "sortedDeep"
        ));
    }

    @Test
    void anyOfComparison() throws Exception {
        assertTrue(OutputComparator.compare(mapper.readTree("[\"aba\", \"bab\"]"), mapper.readTree("\"bab\""), "anyOf"));
        assertFalse(OutputComparator.compare(mapper.readTree("[\"aba\", \"bab\"]"), mapper.readTree("\"abc\""), "anyOf"));
    }
}
