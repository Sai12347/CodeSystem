import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const slidingWindowMetadata: AlgorithmMetadata = {
  id: 'sliding-window',
  title: 'Sliding Window (Max Sum Subarray of Size K)',
  category: 'INTERMEDIATE',
  subcategory: 'Algorithmic Patterns',
  difficulty: 'Medium',
  description:
    'Maintains a fixed-size contiguous window that slides across the array, adding the incoming element and subtracting the outgoing element in O(1) per step.',
  realWorldExample:
    'Calculating rolling 7-day average temperatures or continuous moving averages in financial charts.',
  timeComplexity: {
    best: 'O(n)',
    average: 'O(n)',
    worst: 'O(n)',
  },
  spaceComplexity: 'O(1) auxiliary space',
  commonMistakes: [
    'Recalculating the window sum from scratch each time (O(n*k) naive approach) instead of subtracting leaving item.',
    'Window boundary confusion (off by one between k and index i).',
  ],
  defaultInput: {
    array: [2, 1, 5, 1, 3, 2],
    k: 3,
  },
  code: {
    java: `public int maxSubArrayLenK(int[] arr, int k) {
    int maxSum = 0, windowSum = 0;
    for (int i = 0; i < k; i++) {
        windowSum += arr[i];
    }
    maxSum = windowSum;
    for (int i = k; i < arr.length; i++) {
        windowSum += arr[i] - arr[i - k];
        maxSum = Math.max(maxSum, windowSum);
    }
    return maxSum;
}`,
    python: `def max_sub_array_len_k(arr, k):
    window_sum = sum(arr[:k])
    max_sum = window_sum
    for i in range(k, len(arr)):
        window_sum += arr[i] - arr[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum`,
  },
};

export function generateSlidingWindowSteps(arr: number[], k: number): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const n = arr.length;
  const maxVal = Math.max(...arr, 1);

  const getVisualElements = (
    windowStart: number,
    windowEnd: number,
    incomingIdx?: number,
    outgoingIdx?: number
  ): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      const labels: string[] = [];

      if (idx >= windowStart && idx <= windowEnd) {
        state = 'window';
      }

      if (idx === windowStart) labels.push('start');
      if (idx === windowEnd) labels.push('end');
      if (idx === incomingIdx) {
        state = 'active';
        labels.push('+in');
      }
      if (idx === outgoingIdx) {
        state = 'eliminated';
        labels.push('-out');
      }

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

  let windowSum = 0;
  for (let i = 0; i < k; i++) {
    windowSum += arr[i];
  }
  let maxSum = windowSum;

  steps.push({
    stepIndex: steps.length,
    description: `Build initial window of size k = ${k}. First window sum = ${windowSum}.`,
    elements: getVisualElements(0, k - 1),
    variables: { k, windowStart: 0, windowEnd: k - 1, windowSum, maxSum },
    changedVariables: ['windowSum', 'maxSum'],
    codeLine: { java: 4, python: 2 },
    explanation: {
      why: `Sum first ${k} elements [0 ... ${k - 1}] to form initial baseline.`,
      whatNext: 'Begin sliding window rightwards one element at a time.',
      keyTakeaway: 'The window encapsulates exactly k items.',
    },
  });

  for (let i = k; i < n; i++) {
    const outgoing = arr[i - k];
    const incoming = arr[i];
    const oldSum = windowSum;
    windowSum += incoming - outgoing;
    maxSum = Math.max(maxSum, windowSum);

    steps.push({
      stepIndex: steps.length,
      description: `Slide window to index ${i}: Subtract arr[${i - k}] (${outgoing}), add arr[${i}] (${incoming}). New windowSum = ${windowSum}.`,
      elements: getVisualElements(i - k + 1, i, i, i - k),
      variables: {
        windowStart: i - k + 1,
        windowEnd: i,
        outgoing,
        incoming,
        windowSum,
        maxSum,
      },
      changedVariables: ['windowSum', 'maxSum'],
      codeLine: { java: 8, python: 5 },
      explanation: {
        why: `windowSum = ${oldSum} - ${outgoing} + ${incoming} = ${windowSum}. Done in O(1) arithmetic!`,
        whatNext: 'Update maxSum if windowSum > maxSum.',
        keyTakeaway: 'Never re-sum the whole window; update only the delta.',
      },
    });
  }

  steps.push({
    stepIndex: steps.length,
    description: `Sliding Window complete! Maximum sum of any subarray of size ${k} is ${maxSum}.`,
    elements: getVisualElements(n - k, n - 1),
    variables: { result: maxSum, complete: true },
    changedVariables: ['result'],
    codeLine: { java: 11, python: 7 },
    explanation: {
      why: 'Checked all possible windows in O(n) total operations.',
      whatNext: 'Done.',
      keyTakeaway: 'Sliding window converts O(n*k) into pure linear O(n).',
    },
  });

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
