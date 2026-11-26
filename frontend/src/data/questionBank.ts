/// <reference types="vite/client" />

/**
 * Practice questions are loaded from the curated, validated problem bank in
 * `frontend/src/data/problems`. Those records include the real statement,
 * examples, starter code, reference solution, and test counts.
 */

export type Difficulty = 'Easy' | 'Medium' | 'Hard' | 'Expert';

export interface VisualElementFrame {
  id: string;
  value: number | string;
  state: 'default' | 'comparing' | 'swapping' | 'sorted' | 'active' | 'found' | 'eliminated' | 'pivot' | 'window';
  label?: string;
  subLabel?: string;
}

export interface QuestionAnimationStep {
  stepIndex: number;
  description: string;
  elements: VisualElementFrame[];
  variables: Record<string, string | number | boolean | null>;
  explanation: string;
}

export interface QuestionItem {
  id: string;
  number: number;
  topic: string;
  topicId: string;
  subtopic: string;
  title: string;
  slug: string;
  difficulty: Difficulty;
  companyTag: string;
  description: string;
  realWorldAnalogy: string;
  constraints: string[];
  examples: { input: string; output: string; explanation?: string }[];
  starterCode: { java: string; python: string };
  solutionCode: { java: string; python: string };
  hints: string[];
  timeComplexity: string;
  spaceComplexity: string;
  sampleArray: number[];
  animationSteps: QuestionAnimationStep[];
  visibleTestCount: number;
  hiddenTestCount: number;
}

interface PublicProblem {
  id: string;
  order: number;
  topicId: string;
  topic: string;
  title: string;
  slug: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  subtopic: string;
  companies: string[];
  description: string;
  constraints: string[];
  hints: string[];
  timeComplexity: string;
  spaceComplexity: string;
  examples: QuestionItem['examples'];
  starterCode: QuestionItem['starterCode'];
  solutionCode: QuestionItem['solutionCode'];
  sampleArray?: number[];
  visibleTestCount: number;
  hiddenTestCount: number;
  number: number;
}

const problemModules = import.meta.glob('./problems/*.json', {
  eager: true,
  import: 'default',
}) as Record<string, PublicProblem[]>;

const allQuestions: QuestionItem[] = Object.values(problemModules)
  .flatMap((problems) => problems)
  .map((problem) => ({
    ...problem,
    id: `${problem.topicId}_${problem.slug}`,
    companyTag: problem.companies.length ? problem.companies.join(', ') : 'Practice',
    // The curated problem format does not claim an unverified company-specific
    // real-world use case, so the UI leaves this optional panel out.
    realWorldAnalogy: '',
    sampleArray: problem.sampleArray ?? [],
    animationSteps: [],
  }))
  .sort((a, b) => a.topicId.localeCompare(b.topicId) || a.number - b.number);

const QUESTIONS_BY_TOPIC = new Map<string, QuestionItem[]>();
for (const question of allQuestions) {
  const topicQuestions = QUESTIONS_BY_TOPIC.get(question.topicId) ?? [];
  topicQuestions.push(question);
  QUESTIONS_BY_TOPIC.set(question.topicId, topicQuestions);
}

export function getQuestionsForTopic(topicId: string): QuestionItem[] {
  if (topicId === 'All') return allQuestions;
  return QUESTIONS_BY_TOPIC.get(topicId) ?? [];
}

export function getAllQuestions(): QuestionItem[] {
  return allQuestions;
}

export function getAvailableQuestionTopicIds(): string[] {
  return [...QUESTIONS_BY_TOPIC.keys()];
}

export function getTotalQuestionsCount(): number {
  return allQuestions.length;
}

export const ALL_QUESTIONS = getQuestionsForTopic('arrays');
