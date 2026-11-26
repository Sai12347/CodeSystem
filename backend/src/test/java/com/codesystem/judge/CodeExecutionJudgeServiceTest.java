package com.codesystem.judge;

import com.codesystem.judge.JudgeModels.JudgeRequest;
import com.codesystem.judge.JudgeModels.JudgeResponse;
import com.codesystem.judge.JudgeModels.TestCaseVerdict;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class CodeExecutionJudgeServiceTest {

    private static ProblemBankRepository repository;
    private static CodeExecutionJudgeService judgeService;

    @BeforeAll
    static void setup() {
        ObjectMapper mapper = new ObjectMapper();
        repository = new ProblemBankRepository(mapper);
        repository.loadProblems();
        judgeService = new CodeExecutionJudgeService(repository, mapper, 2, 15, 10, 2500, "");
    }

    @Test
    void bankLoadsProblemsWithHiddenTests() {
        assertTrue(repository.count() >= 1, "Expected problems loaded from classpath:problems/*.json");
        assertTrue(repository.getTotalHiddenTests() >= 8, "Expected hidden tests loaded");
    }

    @Test
    void javaAcceptedAndHiddenInputsAreMasked() {
        String code = """
                class Solution {
                    public int[] findMinMax(int[] nums) {
                        int mn = nums[0], mx = nums[0];
                        for (int x : nums) {
                            if (x < mn) mn = x;
                            if (x > mx) mx = x;
                        }
                        return new int[]{mn, mx};
                    }
                }
                """;
        JudgeResponse resp = judgeService.evaluate(new JudgeRequest("find-min-max", "java", code), false);
        assertEquals("ACCEPTED", resp.status());
        assertEquals(resp.totalCount(), resp.passedCount());
        assertTrue(resp.hiddenTotal() >= 8);
        assertEquals(resp.hiddenTotal(), resp.hiddenPassed());
        for (TestCaseVerdict v : resp.results()) {
            if (v.hidden()) {
                assertNull(v.input(), "Hidden input must never leak");
                assertNull(v.expected(), "Hidden expected output must never leak");
                assertNull(v.actual(), "Hidden actual output must never leak");
            } else {
                assertNotNull(v.input());
                assertNotNull(v.expected());
            }
        }
    }

    @Test
    void pythonWrongAnswerAndCompileErrorHandled() {
        String wrong = "class Solution:\n    def findMinMax(self, nums):\n        return [0, 0]\n";
        JudgeResponse resp = judgeService.evaluate(new JudgeRequest("find-min-max", "python", wrong), false);
        assertEquals("WRONG_ANSWER", resp.status());
        assertTrue(resp.passedCount() < resp.totalCount());

        String badJava = "class Solution { public int[] findMinMax(int[] nums) { return broken; } }";
        JudgeResponse comp = judgeService.evaluate(new JudgeRequest("find-min-max", "java", badJava), true);
        assertEquals("COMPILATION_ERROR", comp.status());
        assertNotNull(comp.compileError());
    }
}
