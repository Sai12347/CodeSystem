package com.codesystem.judge;

import com.codesystem.judge.JudgeModels.JudgeRequest;
import com.codesystem.judge.JudgeModels.JudgeResponse;
import com.codesystem.judge.JudgeModels.TestCaseVerdict;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import com.fasterxml.jackson.databind.node.ObjectNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.ClassPathResource;
import org.springframework.stereotype.Service;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.ArrayList;
import java.util.Comparator;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Locale;
import java.util.Map;
import java.util.concurrent.Semaphore;
import java.util.concurrent.TimeUnit;
import java.util.regex.Pattern;
import java.util.stream.Stream;

/**
 * Compiles and executes user Java 21 or Python 3 submissions against visible and hidden test suites
 * using isolated temporary workspaces and strict time limits.
 */
@Service
public class CodeExecutionJudgeService {

    private static final int MAX_CODE_BYTES = 65_536;
    private static final String JAVA_IMPORT_LINE =
            "import java.util.*; import java.util.function.*; import java.util.stream.*; import java.math.*;";
    private static final String PY_PRELUDE_LINE =
            "from judge_prelude import *  # noqa: F401,F403";
    private static final Pattern JAVA_PACKAGE_RE =
            Pattern.compile("(?m)^\\s*package\\s+[\\w.]+\\s*;\\s*$");
    private static final Pattern JAVA_PUBLIC_TYPE_RE =
            Pattern.compile("(?m)^\\s*public\\s+(?=((final|abstract)\\s+)?(class|interface|enum|record)\\b)");

    private final ProblemBankRepository repository;
    private final ObjectMapper objectMapper;
    private final Semaphore concurrencyLimit;
    private final int compileTimeoutSeconds;
    private final int runTimeoutSeconds;
    private final double perTestLimitMs;
    private final String configuredPython;
    private volatile String resolvedPython;

    public CodeExecutionJudgeService(
            ProblemBankRepository repository,
            ObjectMapper objectMapper,
            @Value("${judge.max-concurrent:4}") int maxConcurrent,
            @Value("${judge.compile-timeout-seconds:15}") int compileTimeoutSeconds,
            @Value("${judge.run-timeout-seconds:10}") int runTimeoutSeconds,
            @Value("${judge.per-test-limit-ms:2500}") double perTestLimitMs,
            @Value("${judge.python-command:}") String configuredPython
    ) {
        this.repository = repository;
        this.objectMapper = objectMapper;
        this.concurrencyLimit = new Semaphore(Math.max(1, maxConcurrent));
        this.compileTimeoutSeconds = compileTimeoutSeconds;
        this.runTimeoutSeconds = runTimeoutSeconds;
        this.perTestLimitMs = perTestLimitMs;
        this.configuredPython = configuredPython;
    }

    public JudgeResponse evaluate(JudgeRequest request, boolean visibleOnly) {
        if (request == null || request.problemId() == null || request.problemId().isBlank()) {
            return errorResponse("", "", visibleOnly, "RUNTIME_ERROR", "Missing problemId.");
        }
        String language = request.language() == null ? "" : request.language().trim().toLowerCase(Locale.ROOT);
        if (!language.equals("java") && !language.equals("python")) {
            return errorResponse(request.problemId(), language, visibleOnly, "RUNTIME_ERROR",
                    "Unsupported language '" + language + "'. Use 'java' or 'python'.");
        }
        String code = request.code() == null ? "" : request.code();
        if (code.isBlank()) {
            return errorResponse(request.problemId(), language, visibleOnly, "COMPILATION_ERROR",
                    "Submission code is empty.");
        }
        if (code.getBytes(StandardCharsets.UTF_8).length > MAX_CODE_BYTES) {
            return errorResponse(request.problemId(), language, visibleOnly, "COMPILATION_ERROR",
                    "Submission exceeds 64 KB limit.");
        }

        JsonNode problem = repository.findById(request.problemId()).orElse(null);
        if (problem == null) {
            return errorResponse(request.problemId(), language, visibleOnly, "RUNTIME_ERROR",
                    "Problem '" + request.problemId() + "' not found in judge bank.");
        }

        List<JsonNode> selectedTests = new ArrayList<>();
        for (JsonNode tc : problem.path("tests")) {
            if (!visibleOnly || !tc.path("hidden").asBoolean(false)) {
                selectedTests.add(tc);
            }
        }
        if (selectedTests.isEmpty()) {
            return errorResponse(request.problemId(), language, visibleOnly, "RUNTIME_ERROR",
                    "No test cases configured for problem.");
        }

        boolean acquired = false;
        try {
            acquired = concurrencyLimit.tryAcquire(15, TimeUnit.SECONDS);
            if (!acquired) {
                return errorResponse(request.problemId(), language, visibleOnly, "RUNTIME_ERROR",
                        "Judge is currently busy. Please retry in a few seconds.");
            }
            return executeInSandbox(problem, language, code, selectedTests, visibleOnly);
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            return errorResponse(request.problemId(), language, visibleOnly, "RUNTIME_ERROR",
                    "Execution interrupted.");
        } catch (Exception e) {
            return errorResponse(request.problemId(), language, visibleOnly, "RUNTIME_ERROR",
                    "Internal judge error: " + e.getMessage());
        } finally {
            if (acquired) {
                concurrencyLimit.release();
            }
        }
    }

    public boolean isJavaAvailable() {
        return checkCommand("javac", "-version");
    }

    public boolean isPythonAvailable() {
        return resolvePythonCommand() != null;
    }

    private JudgeResponse executeInSandbox(
            JsonNode problem,
            String language,
            String code,
            List<JsonNode> tests,
            boolean visibleOnly
    ) throws Exception {
        Path workDir = Files.createTempDirectory("cs-judge-");
        try {
            Path testsPath = workDir.resolve("tests.json");
            Path resultsPath = workDir.resolve("results.jsonl");

            ObjectNode payload = objectMapper.createObjectNode();
            payload.set("signature", problem.path("signature"));
            ArrayNode testArray = objectMapper.createArrayNode();
            for (JsonNode tc : tests) {
                ObjectNode item = objectMapper.createObjectNode();
                item.put("id", tc.path("id").asText());
                item.set("input", tc.path("input"));
                testArray.add(item);
            }
            payload.set("tests", testArray);
            objectMapper.writeValue(testsPath.toFile(), payload);

            JsonNode adapterNode = problem.path("adapter");
            String adapterCode = (adapterNode != null && !adapterNode.isNull() && !adapterNode.isMissingNode())
                    ? adapterNode.path(language).asText(null)
                    : null;

            ProcessOutcome outcome;
            if (language.equals("java")) {
                outcome = runJava(workDir, code, adapterCode, testsPath, resultsPath);
            } else {
                outcome = runPython(workDir, code, adapterCode, testsPath, resultsPath);
            }

            if (outcome.compileError != null) {
                return new JudgeResponse(
                        problem.path("id").asText(),
                        language,
                        visibleOnly ? "run" : "submit",
                        "COMPILATION_ERROR",
                        0,
                        tests.size(),
                        0,
                        countVisible(tests),
                        0,
                        countHidden(tests),
                        0.0,
                        outcome.compileError,
                        null,
                        List.of()
                );
            }

            Map<String, JsonNode> rawResults = readJsonlResults(resultsPath);
            return buildVerdictResponse(problem, language, visibleOnly, tests, rawResults, outcome);
        } finally {
            deleteRecursively(workDir);
        }
    }

    private ProcessOutcome runJava(
            Path workDir,
            String code,
            String adapterCode,
            Path testsPath,
            Path resultsPath
    ) throws Exception {
        copyClasspathResource("judge/java/Judge.java", workDir.resolve("Judge.java"));
        copyClasspathResource("judge/java/ListNode.java", workDir.resolve("ListNode.java"));
        copyClasspathResource("judge/java/TreeNode.java", workDir.resolve("TreeNode.java"));
        Files.writeString(workDir.resolve("Solution.java"), prepareJavaSource(code), StandardCharsets.UTF_8);

        List<String> sources = new ArrayList<>();
        sources.add("Judge.java");
        sources.add("ListNode.java");
        sources.add("TreeNode.java");
        sources.add("Solution.java");

        if (adapterCode != null && !adapterCode.isBlank()) {
            Files.writeString(workDir.resolve("Adapter.java"), JAVA_IMPORT_LINE + "\n" + adapterCode, StandardCharsets.UTF_8);
            sources.add("Adapter.java");
        }

        Path outDir = workDir.resolve("out");
        Files.createDirectories(outDir);

        List<String> javacCmd = new ArrayList<>();
        javacCmd.add("javac");
        javacCmd.add("-encoding");
        javacCmd.add("UTF-8");
        javacCmd.add("-nowarn");
        javacCmd.add("-d");
        javacCmd.add(outDir.toString());
        javacCmd.addAll(sources);

        ExecResult compile = runProcess(javacCmd, workDir, Map.of(), compileTimeoutSeconds);
        if (compile.timedOut) {
            return new ProcessOutcome(false, true, "Compilation timed out after " + compileTimeoutSeconds + "s.", "");
        }
        if (compile.exitCode != 0) {
            String msg = sanitizePaths((compile.stdout + "\n" + compile.stderr).trim(), workDir);
            return new ProcessOutcome(false, false, truncate(msg, 4000), "");
        }

        List<String> javaCmd = List.of(
                "java",
                "-Xss64m",
                "-Xmx256m",
                "-cp",
                outDir.toString(),
                "Judge",
                testsPath.toString(),
                resultsPath.toString()
        );
        ExecResult run = runProcess(javaCmd, workDir, Map.of(), runTimeoutSeconds);
        return new ProcessOutcome(run.exitCode == 0 && !run.timedOut, run.timedOut, null,
                sanitizePaths(truncate(run.stderr, 4000), workDir));
    }

    private ProcessOutcome runPython(
            Path workDir,
            String code,
            String adapterCode,
            Path testsPath,
            Path resultsPath
    ) throws Exception {
        String pyCmd = resolvePythonCommand();
        if (pyCmd == null) {
            return new ProcessOutcome(false, false, null, "Python interpreter is not installed on the judge server.");
        }

        copyClasspathResource("judge/python/judge_lib.py", workDir.resolve("judge_lib.py"));
        copyClasspathResource("judge/python/judge_prelude.py", workDir.resolve("judge_prelude.py"));
        copyClasspathResource("judge/python/judge_runner.py", workDir.resolve("judge_runner.py"));
        Files.writeString(workDir.resolve("solution.py"), PY_PRELUDE_LINE + "\n" + code, StandardCharsets.UTF_8);

        if (adapterCode != null && !adapterCode.isBlank()) {
            Files.writeString(workDir.resolve("adapter.py"), adapterCode, StandardCharsets.UTF_8);
        }

        Map<String, String> env = Map.of(
                "PYTHONDONTWRITEBYTECODE", "1",
                "PYTHONIOENCODING", "utf-8",
                "PYTHONHASHSEED", "0"
        );
        List<String> cmd = List.of(pyCmd, "judge_runner.py", testsPath.toString(), resultsPath.toString());
        ExecResult run = runProcess(cmd, workDir, env, runTimeoutSeconds);

        String stderr = sanitizePaths(truncate(run.stderr, 4000), workDir);
        if (!run.timedOut && run.exitCode != 0 && !Files.exists(resultsPath)
                && (stderr.contains("SyntaxError") || stderr.contains("IndentationError"))) {
            return new ProcessOutcome(false, false, stderr, "");
        }
        return new ProcessOutcome(run.exitCode == 0 && !run.timedOut, run.timedOut, null, stderr);
    }

    private JudgeResponse buildVerdictResponse(
            JsonNode problem,
            String language,
            boolean visibleOnly,
            List<JsonNode> tests,
            Map<String, JsonNode> rawResults,
            ProcessOutcome outcome
    ) throws Exception {
        String compareMode = problem.path("compare").asText("exact");
        List<TestCaseVerdict> verdicts = new ArrayList<>(tests.size());

        int passedCount = 0;
        int visiblePassed = 0;
        int visibleTotal = 0;
        int hiddenPassed = 0;
        int hiddenTotal = 0;
        double totalMs = 0.0;

        boolean sawTle = outcome.timedOut;
        boolean sawRuntimeError = false;
        boolean sawWrongAnswer = false;
        String firstError = null;

        for (JsonNode tc : tests) {
            String id = tc.path("id").asText();
            boolean hidden = tc.path("hidden").asBoolean(false);
            if (hidden) hiddenTotal++;
            else visibleTotal++;

            JsonNode res = rawResults.get(id);
            String displayInput = hidden ? null : tc.path("display").asText(null);
            String expectedStr = hidden ? null : objectMapper.writeValueAsString(tc.path("expected"));

            if (res == null) {
                String status = outcome.timedOut ? "TIME_LIMIT_EXCEEDED" : "RUNTIME_ERROR";
                if (outcome.timedOut) sawTle = true;
                else sawRuntimeError = true;
                String err = outcome.timedOut
                        ? "Execution timed out before completing this test case."
                        : (outcome.stderr != null && !outcome.stderr.isBlank()
                        ? outcome.stderr
                        : "Process terminated unexpectedly before completing this test case.");
                if (firstError == null) firstError = err;
                verdicts.add(new TestCaseVerdict(
                        id, hidden, false, status, 0.0,
                        displayInput, expectedStr, null, null,
                        hidden ? (outcome.timedOut ? "Time Limit Exceeded" : "Runtime Error") : err
                ));
                continue;
            }

            double ms = res.path("timeMs").asDouble(0.0);
            totalMs += ms;
            String rawStatus = res.path("status").asText("RUNTIME_ERROR");
            String stdout = hidden ? null : emptyToNull(res.path("stdout").asText(""));

            if (ms > perTestLimitMs) {
                sawTle = true;
                String err = "Test exceeded per-test time limit of " + (int) perTestLimitMs + " ms.";
                if (firstError == null) firstError = err;
                verdicts.add(new TestCaseVerdict(
                        id, hidden, false, "TIME_LIMIT_EXCEEDED", round2(ms),
                        displayInput, expectedStr, null, stdout, err
                ));
                continue;
            }

            if (!"OK".equals(rawStatus)) {
                sawRuntimeError = true;
                String rawErr = res.path("error").asText("Runtime error");
                String safeErr = hidden ? sanitizeHiddenError(rawErr) : rawErr;
                if (firstError == null) firstError = safeErr;
                verdicts.add(new TestCaseVerdict(
                        id, hidden, false, "RUNTIME_ERROR", round2(ms),
                        displayInput, expectedStr, null, stdout, safeErr
                ));
                continue;
            }

            JsonNode actualNode = res.get("output");
            JsonNode expectedNode = tc.get("expected");
            boolean passed = OutputComparator.compare(expectedNode, actualNode, compareMode);
            if (passed) {
                passedCount++;
                if (hidden) hiddenPassed++;
                else visiblePassed++;
            } else {
                sawWrongAnswer = true;
            }

            String actualStr = hidden ? null : objectMapper.writeValueAsString(actualNode);
            verdicts.add(new TestCaseVerdict(
                    id, hidden, passed, passed ? "PASSED" : "WRONG_ANSWER", round2(ms),
                    displayInput, expectedStr, actualStr, stdout, null
            ));
        }

        String overallStatus;
        if (sawTle) overallStatus = "TIME_LIMIT_EXCEEDED";
        else if (sawRuntimeError) overallStatus = "RUNTIME_ERROR";
        else if (sawWrongAnswer || passedCount < tests.size()) overallStatus = "WRONG_ANSWER";
        else overallStatus = "ACCEPTED";

        return new JudgeResponse(
                problem.path("id").asText(),
                language,
                visibleOnly ? "run" : "submit",
                overallStatus,
                passedCount,
                tests.size(),
                visiblePassed,
                visibleTotal,
                hiddenPassed,
                hiddenTotal,
                round2(totalMs),
                null,
                firstError,
                verdicts
        );
    }

    private String sanitizeHiddenError(String rawError) {
        if (rawError == null || rawError.isBlank()) return "Runtime Error on hidden test";
        String firstLine = rawError.split("\\R", 2)[0];
        int colon = firstLine.indexOf(':');
        if (colon > 0) {
            return firstLine.substring(0, colon) + " on hidden test case";
        }
        return "Runtime Error on hidden test case";
    }

    private Map<String, JsonNode> readJsonlResults(Path resultsPath) throws IOException {
        Map<String, JsonNode> map = new LinkedHashMap<>();
        if (!Files.exists(resultsPath)) return map;
        for (String line : Files.readAllLines(resultsPath, StandardCharsets.UTF_8)) {
            String trimmed = line.trim();
            if (!trimmed.isEmpty()) {
                JsonNode node = objectMapper.readTree(trimmed);
                String id = node.path("id").asText("");
                if (!id.isBlank()) {
                    map.put(id, node);
                }
            }
        }
        return map;
    }

    private String prepareJavaSource(String code) {
        String cleaned = JAVA_PACKAGE_RE.matcher(code).replaceAll("");
        cleaned = JAVA_PUBLIC_TYPE_RE.matcher(cleaned).replaceAll("");
        return JAVA_IMPORT_LINE + "\n" + cleaned;
    }

    private void copyClasspathResource(String classpathLocation, Path destination) throws IOException {
        ClassPathResource res = new ClassPathResource(classpathLocation);
        try (InputStream in = res.getInputStream()) {
            Files.copy(in, destination);
        }
    }

    private String resolvePythonCommand() {
        if (resolvedPython != null) return resolvedPython;
        if (configuredPython != null && !configuredPython.isBlank() && checkCommand(configuredPython, "--version")) {
            resolvedPython = configuredPython;
            return resolvedPython;
        }
        for (String candidate : List.of("python3", "python")) {
            if (checkCommand(candidate, "--version")) {
                resolvedPython = candidate;
                return resolvedPython;
            }
        }
        return null;
    }

    private boolean checkCommand(String... command) {
        try {
            Process p = new ProcessBuilder(command).redirectErrorStream(true).start();
            boolean finished = p.waitFor(5, TimeUnit.SECONDS);
            if (!finished) {
                p.destroyForcibly();
                return false;
            }
            return p.exitValue() == 0;
        } catch (Exception e) {
            return false;
        }
    }

    private ExecResult runProcess(List<String> command, Path workDir, Map<String, String> env, int timeoutSeconds)
            throws Exception {
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.directory(workDir.toFile());
        pb.environment().putAll(env);
        Process proc = pb.start();

        ByteArrayOutputStream stdoutBuf = new ByteArrayOutputStream();
        ByteArrayOutputStream stderrBuf = new ByteArrayOutputStream();
        Thread tOut = new Thread(() -> drainStream(proc.getInputStream(), stdoutBuf, 16_384));
        Thread tErr = new Thread(() -> drainStream(proc.getErrorStream(), stderrBuf, 16_384));
        tOut.setDaemon(true);
        tErr.setDaemon(true);
        tOut.start();
        tErr.start();

        boolean finished = proc.waitFor(timeoutSeconds, TimeUnit.SECONDS);
        if (!finished) {
            proc.destroyForcibly();
            proc.waitFor(2, TimeUnit.SECONDS);
        }
        tOut.join(1000);
        tErr.join(1000);

        return new ExecResult(
                finished ? proc.exitValue() : -1,
                !finished,
                stdoutBuf.toString(StandardCharsets.UTF_8),
                stderrBuf.toString(StandardCharsets.UTF_8)
        );
    }

    private void drainStream(InputStream in, ByteArrayOutputStream out, int maxBytes) {
        byte[] buf = new byte[4096];
        int total = 0;
        try {
            int n;
            while ((n = in.read(buf)) != -1) {
                int toWrite = Math.min(n, Math.max(0, maxBytes - total));
                if (toWrite > 0) {
                    out.write(buf, 0, toWrite);
                    total += toWrite;
                }
            }
        } catch (IOException ignored) {
        }
    }

    private void deleteRecursively(Path dir) {
        if (dir == null || !Files.exists(dir)) return;
        try (Stream<Path> walk = Files.walk(dir)) {
            walk.sorted(Comparator.reverseOrder()).forEach(p -> {
                try {
                    Files.deleteIfExists(p);
                } catch (IOException ignored) {
                }
            });
        } catch (IOException ignored) {
        }
    }

    private String sanitizePaths(String text, Path workDir) {
        if (text == null) return "";
        String dirStr = workDir.toAbsolutePath().toString();
        return text.replace(dirStr + "\\", "").replace(dirStr + "/", "").replace(dirStr, "");
    }

    private String truncate(String s, int maxLen) {
        if (s == null || s.length() <= maxLen) return s == null ? "" : s;
        return s.substring(0, maxLen) + "\n... (truncated)";
    }

    private String emptyToNull(String s) {
        return (s == null || s.isEmpty()) ? null : s;
    }

    private double round2(double v) {
        return Math.round(v * 100.0) / 100.0;
    }

    private int countVisible(List<JsonNode> tests) {
        int c = 0;
        for (JsonNode t : tests) if (!t.path("hidden").asBoolean(false)) c++;
        return c;
    }

    private int countHidden(List<JsonNode> tests) {
        int c = 0;
        for (JsonNode t : tests) if (t.path("hidden").asBoolean(false)) c++;
        return c;
    }

    private JudgeResponse errorResponse(String problemId, String language, boolean visibleOnly, String status, String err) {
        return new JudgeResponse(
                problemId,
                language,
                visibleOnly ? "run" : "submit",
                status,
                0, 0, 0, 0, 0, 0,
                0.0,
                "COMPILATION_ERROR".equals(status) ? err : null,
                "COMPILATION_ERROR".equals(status) ? null : err,
                List.of()
        );
    }

    private record ExecResult(int exitCode, boolean timedOut, String stdout, String stderr) {}
    private record ProcessOutcome(boolean ok, boolean timedOut, String compileError, String stderr) {}
}
