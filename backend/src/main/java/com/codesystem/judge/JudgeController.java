package com.codesystem.judge;

import com.codesystem.judge.JudgeModels.JudgeRequest;
import com.codesystem.judge.JudgeModels.JudgeResponse;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.LinkedHashMap;
import java.util.Map;

@RestController
@RequestMapping("/api/judge")
public class JudgeController {

    private final CodeExecutionJudgeService judgeService;
    private final ProblemBankRepository repository;

    public JudgeController(CodeExecutionJudgeService judgeService, ProblemBankRepository repository) {
        this.judgeService = judgeService;
        this.repository = repository;
    }

    @GetMapping("/health")
    public ResponseEntity<Map<String, Object>> health() {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("status", "UP");
        body.put("loadedProblems", repository.count());
        body.put("totalVisibleTests", repository.getTotalVisibleTests());
        body.put("totalHiddenTests", repository.getTotalHiddenTests());
        body.put("javaAvailable", judgeService.isJavaAvailable());
        body.put("pythonAvailable", judgeService.isPythonAvailable());
        return ResponseEntity.ok(body);
    }

    @PostMapping("/run")
    public ResponseEntity<JudgeResponse> runSampleTests(@RequestBody JudgeRequest request) {
        return ResponseEntity.ok(judgeService.evaluate(request, true));
    }

    @PostMapping("/submit")
    public ResponseEntity<JudgeResponse> submitSolution(@RequestBody JudgeRequest request) {
        return ResponseEntity.ok(judgeService.evaluate(request, false));
    }
}
