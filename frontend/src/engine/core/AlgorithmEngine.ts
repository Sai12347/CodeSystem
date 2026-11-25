import { AlgorithmId, AlgorithmStep, AlgorithmMetadata } from '../../types/algorithm';
import { generateBinarySearchSteps, binarySearchMetadata } from '../algorithms/searching/binarySearch';
import { generateLinearSearchSteps, linearSearchMetadata } from '../algorithms/searching/linearSearch';
import { generateBubbleSortSteps, bubbleSortMetadata } from '../algorithms/sorting/bubbleSort';
import { generateInsertionSortSteps, insertionSortMetadata } from '../algorithms/sorting/insertionSort';
import { generateSelectionSortSteps, selectionSortMetadata } from '../algorithms/sorting/selectionSort';
import { generateMergeSortSteps, mergeSortMetadata } from '../algorithms/sorting/mergeSort';
import { generateQuickSortSteps, quickSortMetadata } from '../algorithms/sorting/quickSort';
import { generateTwoPointersSteps, twoPointersMetadata } from '../algorithms/patterns/twoPointers';
import { generateSlidingWindowSteps, slidingWindowMetadata } from '../algorithms/patterns/slidingWindow';
import { generateStackSteps, stackMetadata } from '../algorithms/dataStructures/stackVisualizer';
import { generateQueueSteps, queueMetadata } from '../algorithms/dataStructures/queueVisualizer';

export interface AlgorithmDefinition {
  metadata: AlgorithmMetadata;
  generateSteps: (input: any, options?: any) => AlgorithmStep[];
}

export const ALGORITHM_REGISTRY: Record<AlgorithmId, AlgorithmDefinition> = {
  'binary-search': {
    metadata: binarySearchMetadata,
    generateSteps: (input: { array: number[]; target: number }) => generateBinarySearchSteps(input.array, input.target),
  },
  'linear-search': {
    metadata: linearSearchMetadata,
    generateSteps: (input: { array: number[]; target: number }) => generateLinearSearchSteps(input.array, input.target),
  },
  'bubble-sort': {
    metadata: bubbleSortMetadata,
    generateSteps: (input: number[]) => generateBubbleSortSteps(input),
  },
  'insertion-sort': {
    metadata: insertionSortMetadata,
    generateSteps: (input: number[]) => generateInsertionSortSteps(input),
  },
  'selection-sort': {
    metadata: selectionSortMetadata,
    generateSteps: (input: number[]) => generateSelectionSortSteps(input),
  },
  'merge-sort': {
    metadata: mergeSortMetadata,
    generateSteps: (input: number[]) => generateMergeSortSteps(input),
  },
  'quick-sort': {
    metadata: quickSortMetadata,
    generateSteps: (input: number[]) => generateQuickSortSteps(input),
  },
  'two-pointers': {
    metadata: twoPointersMetadata,
    generateSteps: (input: { array: number[]; target: number }) => generateTwoPointersSteps(input.array, input.target),
  },
  'sliding-window': {
    metadata: slidingWindowMetadata,
    generateSteps: (input: { array: number[]; k: number }) => generateSlidingWindowSteps(input.array, input.k),
  },
  'stack': {
    metadata: stackMetadata,
    generateSteps: (input: string[]) => generateStackSteps(input),
  },
  'queue': {
    metadata: queueMetadata,
    generateSteps: (input: string[]) => generateQueueSteps(input),
  },
};

export class AlgorithmEngine {
  private steps: AlgorithmStep[] = [];
  private currentStepIndex: number = 0;
  private currentAlgorithmId: AlgorithmId = 'binary-search';

  constructor(algorithmId: AlgorithmId = 'binary-search', input?: any) {
    this.loadAlgorithm(algorithmId, input);
  }

  public loadAlgorithm(algorithmId: AlgorithmId, customInput?: any): void {
    const algo = ALGORITHM_REGISTRY[algorithmId];
    if (!algo) {
      throw new Error(`Algorithm with id ${algorithmId} not found in registry.`);
    }

    this.currentAlgorithmId = algorithmId;
    const input = customInput !== undefined ? customInput : algo.metadata.defaultInput;
    this.steps = algo.generateSteps(input);
    this.currentStepIndex = 0;
  }

  public getSteps(): AlgorithmStep[] {
    return this.steps;
  }

  public getTotalSteps(): number {
    return this.steps.length;
  }

  public getCurrentIndex(): number {
    return this.currentStepIndex;
  }

  public getCurrentStep(): AlgorithmStep {
    if (this.steps.length === 0) {
      return {
        stepIndex: 0,
        description: 'No steps generated.',
        elements: [],
        variables: {},
        codeLine: { java: 1, python: 1 },
        explanation: { why: '', whatNext: '', keyTakeaway: '' },
      };
    }
    return this.steps[this.currentStepIndex];
  }

  public nextStep(): AlgorithmStep | null {
    if (this.currentStepIndex < this.steps.length - 1) {
      this.currentStepIndex++;
      return this.steps[this.currentStepIndex];
    }
    return null;
  }

  public previousStep(): AlgorithmStep | null {
    if (this.currentStepIndex > 0) {
      this.currentStepIndex--;
      return this.steps[this.currentStepIndex];
    }
    return null;
  }

  public jumpToStep(index: number): AlgorithmStep {
    if (index >= 0 && index < this.steps.length) {
      this.currentStepIndex = index;
    }
    return this.getCurrentStep();
  }

  public reset(): AlgorithmStep {
    this.currentStepIndex = 0;
    return this.getCurrentStep();
  }

  public getMetadata(): AlgorithmMetadata {
    return ALGORITHM_REGISTRY[this.currentAlgorithmId].metadata;
  }
}
