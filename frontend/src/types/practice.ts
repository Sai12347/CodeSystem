export interface TestCase {
  id: string;
  input: string;
  expectedOutput: string;
  isHidden: boolean;
}

export interface PracticeProblem {
  id: string;
  title: string;
  slug: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  category: string;
  description: string;
  constraints: string[];
  examples: {
    input: string;
    output: string;
    explanation?: string;
  }[];
  starterCode: {
    java: string;
    python: string;
  };
  solutionCode: {
    java: string;
    python: string;
  };
  testCases: TestCase[];
  hints: string[];
  timeComplexityOptimal: string;
  spaceComplexityOptimal: string;
}

export interface ExecutionResult {
  status: 'ACCEPTED' | 'WRONG_ANSWER' | 'TIME_LIMIT_EXCEEDED' | 'RUNTIME_ERROR' | 'COMPILATION_ERROR';
  passedCount: number;
  totalCount: number;
  executionTimeMs: number;
  memoryMb: number;
  output?: string;
  error?: string;
  details?: {
    testCaseId: string;
    passed: boolean;
    actualOutput: string;
    expectedOutput: string;
  }[];
}
