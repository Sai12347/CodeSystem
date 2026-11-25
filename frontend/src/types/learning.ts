export interface TopicItem {
  id: string;
  title: string;
  category: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
  description: string;
  realWorldExample: string;
  timeComplexity: {
    best: string;
    average: string;
    worst: string;
  };
  spaceComplexity: string;
  commonMistakes: string[];
  javaCode: string;
  pythonCode: string;
  dryRunSteps: {
    step: number;
    action: string;
    state: string;
  }[];
  practiceQuestions: {
    id: string;
    title: string;
    difficulty: 'Easy' | 'Medium' | 'Hard';
    leetcodeSlug?: string;
  }[];
}

export interface CategoryGroup {
  id: 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';
  title: string;
  description: string;
  topics: TopicItem[];
}
