package com.codesystem.controller;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/ai-tutor")
public class AiTutorController {

    @Value("${gemini.api.key:}")
    private String geminiApiKey;

    private final RestTemplate restTemplate = new RestTemplate();

    public record TutorRequest(String query, String topic, String userLevel) {}

    @PostMapping("/explain")
    public ResponseEntity<Map<String, Object>> explainAlgorithm(@RequestBody TutorRequest request) {
        // High-level safe system prompt for Gemini
        String systemInstruction = """
            You are CodeSystem AI Tutor, an elite DSA educator.
            Explain algorithms in a structured, accessible, beginner-friendly format:
            1. Intuitive high-level explanation (plain English, no jargon).
            2. Concrete small example & dry run.
            3. Time and Space complexity breakdown.
            4. Code snippet in Java or Python.
            5. Socratic hint or follow-up question.
            Do not provide complete code solutions directly when answering practice questions; provide hints first.
            """;

        Map<String, Object> response = new HashMap<>();

        if (geminiApiKey == null || geminiApiKey.isBlank()) {
            // Server-side fallback if Gemini key is not yet configured in environment
            response.put("source", "local_fallback");
            response.put("explanation", """
                ### CodeSystem AI Tutor
                
                **Question:** """ + request.query() + """
                
                1. **Intuitive Insight:** In DSA, choosing the right invariant guarantees logarithmic or linear convergence while avoiding redundant state calculations.
                2. **Step-by-Step Dry Run:** Trace each variable step through the array boundaries.
                3. **Complexity:** Time complexity is determined by the number of remaining candidate elements after each comparison.
                
                *Tip: Set GEMINI_API_KEY in backend environment to unlock real-time Gemini LLM answers.*
                """);
            return ResponseEntity.ok(response);
        }

        try {
            String geminiUrl = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + geminiApiKey;

            Map<String, Object> body = Map.of(
                "contents", List.of(
                    Map.of("role", "user", "parts", List.of(
                        Map.of("text", systemInstruction + "\n\nStudent Query: " + request.query())
                    ))
                )
            );

            Map result = restTemplate.postForObject(geminiUrl, body, Map.class);
            response.put("source", "gemini_api");
            response.put("data", result);
            return ResponseEntity.ok(response);
        } catch (Exception e) {
            response.put("error", "AI service temporarily unavailable: " + e.getMessage());
            return ResponseEntity.status(503).body(response);
        }
    }
}
