package com.codesystem.judge;

import java.util.List;

public final class JudgeModels {

    private JudgeModels() {}

    public record JudgeRequest(
            String problemId,
            String language,
            String code
    ) {}

    public record TestCaseVerdict(
            String id,
            boolean hidden,
            boolean passed,
            String status,
            double timeMs,
            String input,
            String expected,
            String actual,
            String stdout,
            String error
    ) {}

    public record JudgeResponse(
            String problemId,
            String language,
            String mode,
            String status,
            int passedCount,
            int totalCount,
            int visiblePassed,
            int visibleTotal,
            int hiddenPassed,
            int hiddenTotal,
            double executionTimeMs,
            String compileError,
            String error,
            List<TestCaseVerdict> results
    ) {}
}
