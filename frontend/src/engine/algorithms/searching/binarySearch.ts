import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const binarySearchMetadata: AlgorithmMetadata = {
  id: 'binary-search',
  title: 'Binary Search',
  category: 'BEGINNER',
  subcategory: 'Searching Algorithms',
  difficulty: 'Easy',
  description:
    'An efficient search algorithm that finds the position of a target value within a sorted array by repeatedly dividing the search interval in half.',
  realWorldExample:
    'Looking up a word in a printed physical dictionary: you open directly to the middle, check if your target word comes before or after, and discard half of the book with every flip.',
  timeComplexity: {
    best: 'O(1) (target is right at the initial middle)',
    average: 'O(log n)',
    worst: 'O(log n) (target at boundaries or not found)',
  },
  spaceComplexity: 'O(1) auxiliary space (iterative)',
  commonMistakes: [
    'Applying binary search on an unsorted array without sorting first.',
    'Integer overflow in (low + high) / 2 in languages with fixed integer limits (better: low + (high - low) / 2).',
    'Off-by-one errors in while condition: using "low < high" instead of "low <= high", which misses 1-element subarrays.',
    'Incorrect pointer updates: forgetting the "+ 1" or "- 1" resulting in an infinite loop.',
  ],
  defaultInput: {
    array: [2, 5, 8, 12, 16, 23, 38],
    target: 16,
  },
  code: {
    java: `public int binarySearch(int[] arr, int target) {
    int low = 0;
    int high = arr.length - 1;
    while (low <= high) {
        int mid = low + (high - low) / 2;
        if (arr[mid] == target) {
            return mid;
        } else if (arr[mid] < target) {
            low = mid + 1;
        } else {
            high = mid - 1;
        }
    }
    return -1;
}`,
    python: `def binary_search(arr, target):
    low = 0
    high = len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1`,
  },
};

export function generateBinarySearchSteps(arr: number[], target: number): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const sortedArr = [...arr].sort((a, b) => a - b);
  const n = sortedArr.length;

  // Step 0: Initial Setup
  const initialElements: VisualElement[] = sortedArr.map((val, idx) => ({
    id: `elem-${idx}-${val}`,
    value: val,
    state: 'default',
    label: idx.toString(),
  }));

  steps.push({
    stepIndex: steps.length,
    description: `Initialize binary search for target = ${target} on sorted array of size ${n}.`,
    elements: initialElements.map((el) => ({ ...el })),
    variables: {
      low: null,
      high: null,
      mid: null,
      'arr[mid]': null,
      target: target,
    },
    changedVariables: ['target'],
    codeLine: { java: 1, python: 1 },
    explanation: {
      why: 'We start by ensuring the array is sorted and establishing target to look for.',
      whatNext: 'Initialize pointers low = 0 and high = length - 1.',
      keyTakeaway: 'Binary search requires a sorted array to guarantee the divide-and-conquer invariant.',
    },
  });

  let low = 0;
  let high = n - 1;

  // Step 1: Pointers initialized
  const buildElements = (
    cLow: number,
    cHigh: number,
    cMid: number | null,
    midState: 'comparing' | 'found' = 'comparing'
  ): VisualElement[] => {
    return sortedArr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      let subLabel = '';

      if (idx < cLow || idx > cHigh) {
        state = 'eliminated';
      } else if (idx === cMid) {
        state = midState;
      } else {
        state = 'active';
      }

      const labels: string[] = [];
      if (idx === cLow) labels.push('low');
      if (idx === cHigh) labels.push('high');
      if (idx === cMid) labels.push('mid');

      if (labels.length > 0) {
        subLabel = labels.join(' & ');
      }

      return {
        id: `elem-${idx}-${val}`,
        value: val,
        state,
        label: `${idx}`,
        subLabel,
        heightPercent: Math.max(20, Math.min(100, (val / Math.max(...sortedArr, 1)) * 100)),
      };
    });
  };

  steps.push({
    stepIndex: steps.length,
    description: `Set search boundaries: low = 0 (val: ${sortedArr[0]}), high = ${high} (val: ${sortedArr[high]}).`,
    elements: buildElements(low, high, null),
    variables: {
      low: low,
      high: high,
      mid: null,
      'arr[mid]': null,
      target: target,
    },
    changedVariables: ['low', 'high'],
    codeLine: { java: 2, python: 2 },
    explanation: {
      why: 'Search boundaries encompass the entire array [0 ... n-1].',
      whatNext: 'Check if low <= high to continue loop.',
      keyTakeaway: 'All candidate answers currently reside between index low and high.',
    },
  });

  let foundIndex = -1;

  while (low <= high) {
    // Step: check while condition
    steps.push({
      stepIndex: steps.length,
      description: `Evaluate loop condition: low (${low}) <= high (${high}) is TRUE.`,
      elements: buildElements(low, high, null),
      variables: {
        low,
        high,
        mid: null,
        'arr[mid]': null,
        target,
      },
      codeLine: { java: 4, python: 4 },
      explanation: {
        why: 'The search space is valid and contains at least one candidate element.',
        whatNext: 'Compute midpoint mid = low + (high - low) / 2.',
        keyTakeaway: 'The loop terminates when low > high, meaning search space is exhausted.',
      },
    });

    const mid = Math.floor(low + (high - low) / 2);
    const midVal = sortedArr[mid];

    // Predict Mode challenge before computing/inspecting mid
    const predictQuestion: AlgorithmStep['prediction'] = {
      question: `Given low = ${low} and high = ${high}, what will be the index of mid?`,
      options: [
        `${Math.floor((low + high) / 2)}`,
        `${Math.max(0, low - 1)}`,
        `${Math.min(n - 1, high + 1)}`,
        `${high}`,
      ],
      correctOptionIndex: 0,
      explanation: `mid = low + Math.floor((high - low) / 2) = ${low} + Math.floor(${high - low} / 2) = ${mid}.`,
      hint: 'Find the integer average of low and high.',
    };

    // Step: compute mid
    steps.push({
      stepIndex: steps.length,
      description: `Compute midpoint index mid = ${mid}. Element at mid is arr[${mid}] = ${midVal}.`,
      elements: buildElements(low, high, mid, 'comparing'),
      variables: {
        low,
        high,
        mid,
        'arr[mid]': midVal,
        target,
      },
      changedVariables: ['mid', 'arr[mid]'],
      codeLine: { java: 5, python: 5 },
      prediction: predictQuestion,
      explanation: {
        why: `We probe the exact middle to discard 50% of the remaining search space with one comparison.`,
        whatNext: `Compare arr[mid] (${midVal}) with target (${target}).`,
        keyTakeaway: 'Probing the middle is what yields O(log n) logarithmic complexity.',
      },
    });

    // Step: compare arr[mid] with target
    steps.push({
      stepIndex: steps.length,
      description: `Compare arr[mid] (${midVal}) with target (${target}).`,
      elements: buildElements(low, high, mid, 'comparing'),
      variables: {
        low,
        high,
        mid,
        'arr[mid]': midVal,
        target,
      },
      codeLine: { java: 6, python: 6 },
      explanation: {
        why: `Checking if arr[mid] == target (${midVal} == ${target}) => ${midVal === target ? 'MATCH' : 'NO MATCH'}.`,
        whatNext:
          midVal === target
            ? 'Return mid index.'
            : midVal < target
            ? 'Target is larger: shift search space to the right half.'
            : 'Target is smaller: shift search space to the left half.',
        keyTakeaway: 'Because the array is sorted, comparing to mid tells us which half the target MUST be in.',
      },
    });

    if (midVal === target) {
      foundIndex = mid;
      steps.push({
        stepIndex: steps.length,
        description: `MATCH FOUND! arr[${mid}] (${midVal}) === target (${target}). Search successful at index ${mid}!`,
        elements: buildElements(low, high, mid, 'found'),
        variables: {
          low,
          high,
          mid,
          'arr[mid]': midVal,
          target,
          result: mid,
        },
        changedVariables: ['result'],
        codeLine: { java: 7, python: 7 },
        explanation: {
          why: `Target ${target} matches the element at index ${mid}.`,
          whatNext: `Execution finishes and returns index ${mid}.`,
          keyTakeaway: `Successfully found in ${steps.length} steps, vastly faster than linear scan.`,
        },
      });
      break;
    } else if (midVal < target) {
      // Predict question: where will low move?
      const movePredict: AlgorithmStep['prediction'] = {
        question: `Since arr[mid] (${midVal}) < target (${target}), which boundary moves?`,
        options: [
          `low moves to mid + 1 (${mid + 1})`,
          `high moves to mid - 1 (${mid - 1})`,
          `low moves to high`,
          `both low and high stay the same`,
        ],
        correctOptionIndex: 0,
        explanation: `Target is greater than arr[mid], so it can only be in the right half: low = mid + 1.`,
        hint: 'In a sorted array, numbers greater than arr[mid] are to its right.',
      };

      steps.push({
        stepIndex: steps.length,
        description: `arr[mid] (${midVal}) < target (${target}). Target must be in the right half.`,
        elements: buildElements(low, high, mid, 'comparing'),
        variables: {
          low,
          high,
          mid,
          'arr[mid]': midVal,
          target,
        },
        codeLine: { java: 8, python: 8 },
        prediction: movePredict,
        explanation: {
          why: `All elements at indices <= ${mid} are strictly smaller than target. Discard the left half.`,
          whatNext: `Update low = mid + 1 (${mid + 1}).`,
          keyTakeaway: 'We eliminate ~50% of candidate items in a single check.',
        },
      });

      low = mid + 1;
      steps.push({
        stepIndex: steps.length,
        description: `Update low = mid + 1 = ${low}. Search range is now [${low} ... ${high}].`,
        elements: buildElements(low, high, null),
        variables: {
          low,
          high,
          mid,
          'arr[mid]': midVal,
          target,
        },
        changedVariables: ['low'],
        codeLine: { java: 9, python: 9 },
        explanation: {
          why: `Left boundary is updated to explore remaining elements.`,
          whatNext: `Loop back and check low <= high.`,
          keyTakeaway: `Remaining search space reduced from ${high - (low - 1) + 1} to ${high - low + 1} items.`,
        },
      });
    } else {
      // midVal > target
      steps.push({
        stepIndex: steps.length,
        description: `arr[mid] (${midVal}) > target (${target}). Target must be in the left half.`,
        elements: buildElements(low, high, mid, 'comparing'),
        variables: {
          low,
          high,
          mid,
          'arr[mid]': midVal,
          target,
        },
        codeLine: { java: 10, python: 10 },
        explanation: {
          why: `All elements at indices >= ${mid} are strictly larger than target. Discard the right half.`,
          whatNext: `Update high = mid - 1 (${mid - 1}).`,
          keyTakeaway: 'We eliminate ~50% of candidate items in a single check.',
        },
      });

      high = mid - 1;
      steps.push({
        stepIndex: steps.length,
        description: `Update high = mid - 1 = ${high}. Search range is now [${low} ... ${high}].`,
        elements: buildElements(low, high, null),
        variables: {
          low,
          high,
          mid,
          'arr[mid]': midVal,
          target,
        },
        changedVariables: ['high'],
        codeLine: { java: 11, python: 11 },
        explanation: {
          why: `Right boundary is updated to explore remaining elements.`,
          whatNext: `Loop back and check low <= high.`,
          keyTakeaway: `Remaining search space reduced.`,
        },
      });
    }
  }

  if (foundIndex === -1) {
    steps.push({
      stepIndex: steps.length,
      description: `Search space exhausted: low (${low}) > high (${high}). Target ${target} not in array. Return -1.`,
      elements: sortedArr.map((val, idx) => ({
        id: `elem-${idx}-${val}`,
        value: val,
        state: 'eliminated',
        label: `${idx}`,
      })),
      variables: {
        low,
        high,
        mid: null,
        'arr[mid]': null,
        target,
        result: -1,
      },
      changedVariables: ['result'],
      codeLine: { java: 13, python: 12 },
      explanation: {
        why: 'The low pointer crossed high. Target is proven to not exist in the collection.',
        whatNext: 'Algorithm terminates returning -1.',
        keyTakeaway: 'Binary search conclusively proves absence in logarithmic time.',
      },
    });
  }

  // Set totalSteps on each step
  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
