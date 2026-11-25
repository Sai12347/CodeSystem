import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const linearSearchMetadata: AlgorithmMetadata = {
  id: 'linear-search',
  title: 'Linear Search',
  category: 'BEGINNER',
  subcategory: 'Searching Algorithms',
  difficulty: 'Easy',
  description:
    'Sequentially checks each element of the list until a match is found or the whole list has been searched.',
  realWorldExample:
    'Searching for your lost keys in a row of pockets or scanning an unsorted grocery shopping list item by item.',
  timeComplexity: {
    best: 'O(1) (target is at the very first position)',
    average: 'O(n) (target in the middle on average)',
    worst: 'O(n) (target is at the end or absent)',
  },
  spaceComplexity: 'O(1) auxiliary space',
  commonMistakes: [
    'Scanning past the array bounds (index out of range).',
    'Returning -1 inside the loop instead of after checking all elements.',
    'Using linear search on large datasets where sorting + binary search would be drastically faster.',
  ],
  defaultInput: {
    array: [19, 45, 12, 8, 33, 27, 50],
    target: 8,
  },
  code: {
    java: `public int linearSearch(int[] arr, int target) {
    for (int i = 0; i < arr.length; i++) {
        if (arr[i] == target) {
            return i;
        }
    }
    return -1;
}`,
    python: `def linear_search(arr, target):
    for i in range(len(arr)):
        if arr[i] == target:
            return i
    return -1`,
  },
};

export function generateLinearSearchSteps(arr: number[], target: number): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const n = arr.length;

  const buildElements = (currentIndex: number | null, found: boolean = false): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      if (found && idx === currentIndex) {
        state = 'found';
      } else if (currentIndex !== null && idx === currentIndex) {
        state = 'comparing';
      } else if (currentIndex !== null && idx < currentIndex) {
        state = 'eliminated';
      }

      return {
        id: `elem-${idx}-${val}`,
        value: val,
        state,
        label: `${idx}`,
        subLabel: idx === currentIndex ? 'i' : '',
        heightPercent: Math.max(20, Math.min(100, (val / Math.max(...arr, 1)) * 100)),
      };
    });
  };

  steps.push({
    stepIndex: steps.length,
    description: `Begin linear search for target ${target} across array of ${n} elements.`,
    elements: buildElements(null),
    variables: { i: null, 'arr[i]': null, target },
    codeLine: { java: 1, python: 1 },
    explanation: {
      why: 'Starting search from index 0.',
      whatNext: 'Begin iterating with i = 0.',
      keyTakeaway: 'Linear search makes no assumptions about element order.',
    },
  });

  let found = false;
  for (let i = 0; i < n; i++) {
    const val = arr[i];

    steps.push({
      stepIndex: steps.length,
      description: `Check index i = ${i}: arr[${i}] is ${val}. Compare with target ${target}.`,
      elements: buildElements(i, false),
      variables: { i, 'arr[i]': val, target },
      changedVariables: ['i', 'arr[i]'],
      codeLine: { java: 2, python: 2 },
      prediction:
        i === 1
          ? {
              question: `Does arr[${i}] (${val}) equal target (${target})?`,
              options: ['Yes, match found!', 'No, continue search'],
              correctOptionIndex: val === target ? 0 : 1,
              explanation: `${val} ${val === target ? 'equals' : 'does not equal'} target ${target}.`,
              hint: 'Look closely at the current element value.',
            }
          : undefined,
      explanation: {
        why: `Examining element at index ${i}.`,
        whatNext: val === target ? 'Return index i.' : 'Move to index i + 1.',
        keyTakeaway: 'Each comparison eliminates exactly one element.',
      },
    });

    if (val === target) {
      steps.push({
        stepIndex: steps.length,
        description: `MATCH FOUND! arr[${i}] (${val}) matches target (${target}) at index ${i}.`,
        elements: buildElements(i, true),
        variables: { i, 'arr[i]': val, target, result: i },
        changedVariables: ['result'],
        codeLine: { java: 3, python: 3 },
        explanation: {
          why: 'Found target value.',
          whatNext: 'Return index i and terminate.',
          keyTakeaway: 'Best case is O(1) if target is at index 0.',
        },
      });
      found = true;
      break;
    }
  }

  if (!found) {
    steps.push({
      stepIndex: steps.length,
      description: `Reached end of array without finding ${target}. Return -1.`,
      elements: buildElements(n, false),
      variables: { i: n, 'arr[i]': null, target, result: -1 },
      changedVariables: ['result'],
      codeLine: { java: 6, python: 5 },
      explanation: {
        why: 'Checked all n elements.',
        whatNext: 'Return -1 indicating not found.',
        keyTakeaway: 'Worst-case time complexity is O(n).',
      },
    });
  }

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
