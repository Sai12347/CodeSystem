export type AlgorithmId =
  | 'binary-search'
  | 'linear-search'
  | 'bubble-sort'
  | 'insertion-sort'
  | 'selection-sort'
  | 'merge-sort'
  | 'quick-sort'
  | 'two-pointers'
  | 'sliding-window'
  | 'stack'
  | 'queue';

export type ElementState =
  | 'default'
  | 'comparing'
  | 'swapping'
  | 'sorted'
  | 'active'
  | 'found'
  | 'eliminated'
  | 'pivot'
  | 'window'
  | 'target';

export interface VisualElement {
  id: string;
  value: number | string;
  state: ElementState;
  label?: string;
  subLabel?: string;
  isPointer?: boolean;
  heightPercent?: number;
}

export interface CodeHighlight {
  java: number;
  python: number;
}

export interface PredictionChallenge {
  question: string;
  options: string[];
  correctOptionIndex: number;
  explanation: string;
  hint: string;
}

export interface StepExplanation {
  why: string;
  whatNext: string;
  keyTakeaway: string;
}

export interface AlgorithmStep {
  stepIndex: number;
  totalSteps?: number;
  description: string;
  elements: VisualElement[];
  variables: Record<string, string | number | boolean | null>;
  changedVariables?: string[];
  codeLine: CodeHighlight;
  explanation: StepExplanation;
  prediction?: PredictionChallenge;
}

export type AlgorithmCategory = 'BEGINNER' | 'INTERMEDIATE' | 'ADVANCED';

export interface TimeComplexity {
  best: string;
  average: string;
  worst: string;
}

export interface AlgorithmMetadata {
  id: AlgorithmId;
  title: string;
  category: AlgorithmCategory;
  subcategory: string;
  difficulty: 'Easy' | 'Medium' | 'Hard';
  description: string;
  realWorldExample: string;
  timeComplexity: TimeComplexity;
  spaceComplexity: string;
  commonMistakes: string[];
  defaultInput: any;
  code: {
    java: string;
    python: string;
  };
}

export interface PlaybackState {
  isPlaying: boolean;
  currentStepIndex: number;
  speed: number; // 0.25, 0.5, 1, 2, 4
  predictMode: boolean;
  isPredictModalOpen: boolean;
  predictionAnswered: boolean;
  userPredictedCorrectly: boolean | null;
}
