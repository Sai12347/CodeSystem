import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const insertionSortMetadata: AlgorithmMetadata = {
  id: 'insertion-sort',
  title: 'Insertion Sort',
  category: 'BEGINNER',
  subcategory: 'Sorting Algorithms',
  difficulty: 'Easy',
  description:
    'Builds the sorted array one element at a time by repeatedly taking the next element and inserting it into its correct position among the previously sorted elements.',
  realWorldExample:
    'Sorting playing cards in your hand: you take one card at a time and insert it into its correct place among the sorted cards you are already holding.',
  timeComplexity: {
    best: 'O(n) (when already sorted)',
    average: 'O(n²)',
    worst: 'O(n²) (reverse sorted)',
  },
  spaceComplexity: 'O(1) auxiliary space (in-place)',
  commonMistakes: [
    'Overwriting elements when shifting without saving the current element in a "key" variable.',
    'Index out of bounds on the inner while loop condition (forgetting "j >= 0").',
  ],
  defaultInput: [29, 10, 14, 37, 13],
  code: {
    java: `public void insertionSort(int[] arr) {
    for (int i = 1; i < arr.length; i++) {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            j = j - 1;
        }
        arr[j + 1] = key;
    }
}`,
    python: `def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key`,
  },
};

export function generateInsertionSortSteps(initialArr: number[]): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const arr = [...initialArr];
  const n = arr.length;
  const maxVal = Math.max(...arr, 1);

  const getVisualElements = (
    keyIndex: number | null,
    compareIndex: number | null,
    sortedUpTo: number
  ): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      let subLabel = '';

      if (idx === keyIndex) {
        state = 'active';
        subLabel = 'key';
      } else if (idx === compareIndex) {
        state = 'comparing';
        subLabel = 'j';
      } else if (idx <= sortedUpTo) {
        state = 'sorted';
        subLabel = 'sorted';
      }

      return {
        id: `elem-${idx}-${val}`,
        value: val,
        state,
        label: `${idx}`,
        subLabel,
        heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
      };
    });
  };

  steps.push({
    stepIndex: steps.length,
    description: `Begin Insertion Sort. Element at index 0 (${arr[0]}) is trivially considered sorted.`,
    elements: getVisualElements(null, null, 0),
    variables: { i: null, key: null, j: null },
    codeLine: { java: 1, python: 1 },
    explanation: {
      why: 'Single element subarray is inherently sorted.',
      whatNext: 'Start with index i = 1.',
      keyTakeaway: 'The left portion [0...i-1] remains sorted at all times.',
    },
  });

  for (let i = 1; i < n; i++) {
    const key = arr[i];
    let j = i - 1;

    steps.push({
      stepIndex: steps.length,
      description: `Pick key = arr[${i}] (${key}). Insert into sorted prefix [0 ... ${i - 1}].`,
      elements: getVisualElements(i, null, i - 1),
      variables: { i, key, j },
      changedVariables: ['i', 'key', 'j'],
      codeLine: { java: 3, python: 3 },
      explanation: {
        why: `Storing ${key} in temporary variable 'key' before shifting larger elements right.`,
        whatNext: `Compare key (${key}) with sorted elements to its left starting at j = ${j}.`,
        keyTakeaway: 'Elements larger than key will shift one position to the right.',
      },
    });

    while (j >= 0 && arr[j] > key) {
      steps.push({
        stepIndex: steps.length,
        description: `arr[${j}] (${arr[j]}) > key (${key}). Shift arr[${j}] right to index ${j + 1}.`,
        elements: getVisualElements(i, j, i - 1),
        variables: { i, key, j, 'arr[j]': arr[j] },
        codeLine: { java: 5, python: 5 },
        explanation: {
          why: `${arr[j]} is larger than key, so key belongs somewhere to its left.`,
          whatNext: `Copy ${arr[j]} into index ${j + 1}.`,
          keyTakeaway: 'Vacates position for key or for earlier larger elements.',
        },
      });

      arr[j + 1] = arr[j];
      j--;
    }

    arr[j + 1] = key;

    steps.push({
      stepIndex: steps.length,
      description: `Found insertion slot: insert key (${key}) at arr[${j + 1}]. Subarray [0 ... ${i}] is now sorted.`,
      elements: getVisualElements(null, null, i),
      variables: { i, key, j: j + 1, 'insertedAt': j + 1 },
      changedVariables: ['insertedAt'],
      codeLine: { java: 8, python: 8 },
      explanation: {
        why: `j reached -1 or arr[j] <= key, so correct position for key is j + 1 (${j + 1}).`,
        whatNext: i < n - 1 ? 'Move to next index i + 1.' : 'Done!',
        keyTakeaway: `Prefix of length ${i + 1} is now fully sorted.`,
      },
    });
  }

  steps.push({
    stepIndex: steps.length,
    description: `Insertion Sort completed! All ${n} elements are sorted.`,
    elements: getVisualElements(null, null, n - 1),
    variables: { i: n, key: null, j: null },
    codeLine: { java: 10, python: 9 },
    explanation: {
      why: 'All elements processed.',
      whatNext: 'Sorting complete.',
      keyTakeaway: 'Insertion Sort is highly efficient on small or nearly sorted datasets.',
    },
  });

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
