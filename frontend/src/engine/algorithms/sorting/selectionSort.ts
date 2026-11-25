import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const selectionSortMetadata: AlgorithmMetadata = {
  id: 'selection-sort',
  title: 'Selection Sort',
  category: 'BEGINNER',
  subcategory: 'Sorting Algorithms',
  difficulty: 'Easy',
  description:
    'Sorts an array by repeatedly finding the minimum element from the unsorted part and putting it at the beginning.',
  realWorldExample:
    'Picking the shortest person in a crowd to stand first in line, then the shortest of the remaining crowd for the second spot, and so on.',
  timeComplexity: {
    best: 'O(n²)',
    average: 'O(n²)',
    worst: 'O(n²)',
  },
  spaceComplexity: 'O(1) auxiliary space (in-place)',
  commonMistakes: [
    'Thinking selection sort is adaptive or O(n) when sorted (it always makes O(n²) comparisons regardless of input).',
    'Updating min_idx incorrectly in the inner loop.',
  ],
  defaultInput: [64, 25, 12, 22, 11],
  code: {
    java: `public void selectionSort(int[] arr) {
    int n = arr.length;
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIdx]) {
                minIdx = j;
            }
        }
        int temp = arr[minIdx];
        arr[minIdx] = arr[i];
        arr[i] = temp;
    }
}`,
    python: `def selection_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]`,
  },
};

export function generateSelectionSortSteps(initialArr: number[]): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const arr = [...initialArr];
  const n = arr.length;
  const maxVal = Math.max(...arr, 1);

  const getVisualElements = (
    i: number | null,
    j: number | null,
    minIdx: number | null,
    swapping: boolean = false
  ): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      const labels: string[] = [];

      if (i !== null && idx < i) {
        state = 'sorted';
        labels.push('sorted');
      } else if (swapping && (idx === i || idx === minIdx)) {
        state = 'swapping';
      } else if (idx === minIdx) {
        state = 'pivot';
        labels.push('min');
      } else if (idx === j) {
        state = 'comparing';
        labels.push('j');
      }

      if (idx === i) labels.push('i');

      return {
        id: `elem-${idx}-${val}`,
        value: val,
        state,
        label: `${idx}`,
        subLabel: labels.join(', '),
        heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
      };
    });
  };

  steps.push({
    stepIndex: steps.length,
    description: `Start Selection Sort on array of ${n} elements.`,
    elements: getVisualElements(null, null, null),
    variables: { i: null, j: null, minIdx: null },
    codeLine: { java: 1, python: 1 },
    explanation: {
      why: 'Initialize array.',
      whatNext: 'Start outer loop at i = 0.',
      keyTakeaway: 'Selection sort makes at most n swaps, which is optimal for write operations.',
    },
  });

  for (let i = 0; i < n - 1; i++) {
    let minIdx = i;

    steps.push({
      stepIndex: steps.length,
      description: `Step ${i}: Assume minimum is at index i = ${i} (value: ${arr[i]}).`,
      elements: getVisualElements(i, null, minIdx),
      variables: { i, minIdx, 'arr[minIdx]': arr[minIdx] },
      changedVariables: ['i', 'minIdx'],
      codeLine: { java: 4, python: 4 },
      explanation: {
        why: `We search subarray [${i + 1} ... ${n - 1}] to see if anything is smaller than ${arr[i]}.`,
        whatNext: `Scan j from ${i + 1} to ${n - 1}.`,
        keyTakeaway: 'minIdx tracks the index containing the current minimum in unsorted part.',
      },
    });

    for (let j = i + 1; j < n; j++) {
      const isSmaller = arr[j] < arr[minIdx];

      steps.push({
        stepIndex: steps.length,
        description: `Compare arr[${j}] (${arr[j]}) with current minimum arr[${minIdx}] (${arr[minIdx]}).`,
        elements: getVisualElements(i, j, minIdx),
        variables: { i, j, minIdx, 'arr[minIdx]': arr[minIdx], 'arr[j]': arr[j] },
        codeLine: { java: 6, python: 6 },
        explanation: {
          why: `Looking for an element smaller than ${arr[minIdx]}.`,
          whatNext: isSmaller ? `Update minIdx to ${j}!` : 'Keep current minIdx.',
          keyTakeaway: 'Always scans the entire remaining unsorted list.',
        },
      });

      if (isSmaller) {
        minIdx = j;
        steps.push({
          stepIndex: steps.length,
          description: `New minimum found! Updated minIdx = ${minIdx} (value: ${arr[minIdx]}).`,
          elements: getVisualElements(i, j, minIdx),
          variables: { i, j, minIdx, 'arr[minIdx]': arr[minIdx] },
          changedVariables: ['minIdx', 'arr[minIdx]'],
          codeLine: { java: 7, python: 7 },
          explanation: {
            why: `${arr[j]} is smaller than previous minimum.`,
            whatNext: 'Continue scanning remaining elements.',
            keyTakeaway: 'Minimum candidate updated.',
          },
        });
      }
    }

    // Swap arr[i] with arr[minIdx]
    const temp = arr[minIdx];
    arr[minIdx] = arr[i];
    arr[i] = temp;

    steps.push({
      stepIndex: steps.length,
      description: `Swap arr[${i}] (${arr[minIdx]}) with minimum element arr[${minIdx}] (${arr[i]}). Index ${i} sorted!`,
      elements: getVisualElements(i, null, minIdx, true),
      variables: { i, minIdx, 'arr[i]': arr[i] },
      changedVariables: ['arr[i]'],
      codeLine: { java: 11, python: 8 },
      explanation: {
        why: `Smallest remaining element placed at index ${i}.`,
        whatNext: 'Move to next position i + 1.',
        keyTakeaway: `Index 0 through ${i} now fully sorted.`,
      },
    });
  }

  steps.push({
    stepIndex: steps.length,
    description: `Selection Sort completed! Array is fully sorted.`,
    elements: arr.map((val, idx) => ({
      id: `elem-${idx}-${val}`,
      value: val,
      state: 'sorted',
      label: `${idx}`,
      subLabel: 'sorted',
      heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
    })),
    variables: { i: n, minIdx: null },
    codeLine: { java: 13, python: 8 },
    explanation: {
      why: 'All positions filled with minimums.',
      whatNext: 'Finished.',
      keyTakeaway: 'Total comparisons: n*(n-1)/2.',
    },
  });

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
