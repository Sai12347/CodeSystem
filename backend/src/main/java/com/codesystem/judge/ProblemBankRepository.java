package com.codesystem.judge;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import jakarta.annotation.PostConstruct;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.Resource;
import org.springframework.core.io.support.PathMatchingResourcePatternResolver;
import org.springframework.stereotype.Component;

import java.io.InputStream;
import java.util.Collections;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Optional;

/**
 * Loads all generated problem specs (including hidden test cases) from classpath:problems/*.json.
 */
@Component
public class ProblemBankRepository {

    private static final Logger log = LoggerFactory.getLogger(ProblemBankRepository.class);

    private final ObjectMapper objectMapper;
    private Map<String, JsonNode> problemsById = Collections.emptyMap();
    private int totalVisibleTests;
    private int totalHiddenTests;

    public ProblemBankRepository(ObjectMapper objectMapper) {
        this.objectMapper = objectMapper;
    }

    @PostConstruct
    public void loadProblems() {
        Map<String, JsonNode> loaded = new LinkedHashMap<>();
        int visible = 0;
        int hidden = 0;
        try {
            PathMatchingResourcePatternResolver resolver = new PathMatchingResourcePatternResolver();
            Resource[] resources = resolver.getResources("classpath*:problems/*.json");
            for (Resource resource : resources) {
                try (InputStream in = resource.getInputStream()) {
                    JsonNode root = objectMapper.readTree(in);
                    JsonNode problems = root.get("problems");
                    if (problems != null && problems.isArray()) {
                        for (JsonNode p : problems) {
                            String id = p.path("id").asText("");
                            if (!id.isBlank()) {
                                loaded.put(id, p);
                                JsonNode tests = p.get("tests");
                                if (tests != null && tests.isArray()) {
                                    for (JsonNode t : tests) {
                                        if (t.path("hidden").asBoolean(false)) hidden++;
                                        else visible++;
                                    }
                                }
                            }
                        }
                    }
                }
            }
            this.problemsById = Collections.unmodifiableMap(loaded);
            this.totalVisibleTests = visible;
            this.totalHiddenTests = hidden;
            log.info("Loaded {} problems into judge bank ({} visible tests, {} hidden tests)",
                    loaded.size(), visible, hidden);
        } catch (Exception e) {
            log.error("Failed to load judge problem bank", e);
        }
    }

    public Optional<JsonNode> findById(String problemId) {
        return Optional.ofNullable(problemsById.get(problemId));
    }

    public int count() {
        return problemsById.size();
    }

    public int getTotalVisibleTests() {
        return totalVisibleTests;
    }

    public int getTotalHiddenTests() {
        return totalHiddenTests;
    }
}
