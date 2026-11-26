import { Difficulty, QuestionItem, getAllQuestions } from './questionBank';

export type CompanyName =
  | 'Google'
  | 'Amazon'
  | 'Microsoft'
  | 'Meta'
  | 'Apple'
  | 'Netflix'
  | 'Uber'
  | 'Goldman Sachs'
  | 'Adobe'
  | 'Atlassian'
  | 'Salesforce'
  | 'Oracle';

export interface CompanyMeta {
  name: CompanyName;
  slug: string;
  logo: string;
  color: string;
}

export interface CompanyQuestionItem {
  id: string;
  number: number;
  company: CompanyName;
  title: string;
  slug: string;
  topic: string;
  subtopic: string;
  difficulty: Difficulty;
  description: string;
  realWorldAnalogy: string;
  constraints: string[];
  examples: QuestionItem['examples'];
  starterCode: QuestionItem['starterCode'];
  timeComplexity: string;
  spaceComplexity: string;
  sampleArray: number[];
}

export const TOP_MNCS: CompanyMeta[] = [
  { name: 'Google', slug: 'google', logo: 'G', color: 'from-blue-500 to-red-500' },
  { name: 'Amazon', slug: 'amazon', logo: 'A', color: 'from-amber-500 to-orange-600' },
  { name: 'Microsoft', slug: 'microsoft', logo: 'M', color: 'from-blue-600 to-cyan-500' },
  { name: 'Meta', slug: 'meta', logo: 'M', color: 'from-blue-600 to-indigo-700' },
  { name: 'Apple', slug: 'apple', logo: 'A', color: 'from-zinc-700 to-zinc-950' },
  { name: 'Netflix', slug: 'netflix', logo: 'N', color: 'from-red-600 to-rose-900' },
  { name: 'Uber', slug: 'uber', logo: 'U', color: 'from-zinc-800 to-black' },
  { name: 'Goldman Sachs', slug: 'goldman-sachs', logo: 'GS', color: 'from-blue-700 to-sky-900' },
  { name: 'Adobe', slug: 'adobe', logo: 'A', color: 'from-red-500 to-rose-700' },
  { name: 'Atlassian', slug: 'atlassian', logo: 'At', color: 'from-blue-500 to-indigo-600' },
  { name: 'Salesforce', slug: 'salesforce', logo: 'S', color: 'from-sky-500 to-blue-600' },
  { name: 'Oracle', slug: 'oracle', logo: 'O', color: 'from-red-600 to-orange-700' },
];

const COMPANY_QUESTIONS_CACHE: Partial<Record<CompanyName, CompanyQuestionItem[]>> = {};

function mapCompanyProblem(company: CompanyName, problem: QuestionItem, number: number): CompanyQuestionItem {
  return {
    ...problem,
    id: `${company.toLowerCase().replace(/[^a-z0-9]+/g, '_')}_${problem.slug}`,
    number,
    company,
  };
}

export function getQuestionsForCompany(company: CompanyName): CompanyQuestionItem[] {
  if (!COMPANY_QUESTIONS_CACHE[company]) {
    const matching = getAllQuestions().filter((question) => question.companyTag.split(', ').includes(company));
    COMPANY_QUESTIONS_CACHE[company] = matching.map((question, index) =>
      mapCompanyProblem(company, question, index + 1)
    );
  }
  return COMPANY_QUESTIONS_CACHE[company]!;
}
