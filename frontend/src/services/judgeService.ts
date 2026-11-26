export type JudgeStatus =
  | 'ACCEPTED'
  | 'WRONG_ANSWER'
  | 'TIME_LIMIT_EXCEEDED'
  | 'RUNTIME_ERROR'
  | 'COMPILATION_ERROR';

export interface TestCaseVerdict {
  id: string;
  hidden: boolean;
  passed: boolean;
  status: 'PASSED' | 'WRONG_ANSWER' | 'TIME_LIMIT_EXCEEDED' | 'RUNTIME_ERROR';
  timeMs: number;
  input: string | null;
  expected: string | null;
  actual: string | null;
  stdout: string | null;
  error: string | null;
}

export interface JudgeResponse {
  problemId: string;
  language: 'java' | 'python';
  mode: 'run' | 'submit';
  status: JudgeStatus;
  passedCount: number;
  totalCount: number;
  visiblePassed: number;
  visibleTotal: number;
  hiddenPassed: number;
  hiddenTotal: number;
  executionTimeMs: number;
  compileError: string | null;
  error: string | null;
  results: TestCaseVerdict[];
}

export interface JudgeHealth {
  status: string;
  loadedProblems: number;
  totalVisibleTests: number;
  totalHiddenTests: number;
  javaAvailable: boolean;
  pythonAvailable: boolean;
}

const API_BASE = (import.meta as any).env?.VITE_API_BASE_URL || '';

async function postJudge(
  endpoint: '/api/judge/run' | '/api/judge/submit',
  problemId: string,
  language: 'java' | 'python',
  code: string
): Promise<JudgeResponse> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ problemId, language, code }),
    });
  } catch {
    throw new Error(
      'Unable to reach the code judge (/api/judge). Start AlgoPlay with start-algoplay.cmd (or `npm run dev` in the frontend folder), which runs the built-in Java/Python compiler.'
    );
  }

  if (!response.ok) {
    const text = await response.text().catch(() => '');
    throw new Error(`Judge server error (${response.status}): ${text || response.statusText}`);
  }

  return (await response.json()) as JudgeResponse;
}

export const judgeService = {
  runSampleTests(problemId: string, language: 'java' | 'python', code: string): Promise<JudgeResponse> {
    return postJudge('/api/judge/run', problemId, language, code);
  },

  submitSolution(problemId: string, language: 'java' | 'python', code: string): Promise<JudgeResponse> {
    return postJudge('/api/judge/submit', problemId, language, code);
  },

  async checkHealth(): Promise<JudgeHealth | null> {
    try {
      const res = await fetch(`${API_BASE}/api/judge/health`);
      if (!res.ok) return null;
      return (await res.json()) as JudgeHealth;
    } catch {
      return null;
    }
  },
};
