import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const twoPointersMetadata: AlgorithmMetadata = {
  id: 'two-pointers',
  title: 'Two Pointers (Two Sum Sorted)',
  category: 'INTERMEDIATE',
  subcategory: 'Algorithmic Patterns',
  difficulty: 'Easy',
  description:
    'Uses two pointers moving inwards from the edges of a sorted array to locate a pair that sums to a target value in linear time.',
  realWorldExample:
    'Calibrating a scale with two weights from opposite ends of a sorted rack until the sum matches target weight.',
  timeComplexity: {
    best: 'O(1) (sum matches on first check)',
    average: 'O(n)',
    worst: 'O(n)',
  },
  spaceComplexity: 'O(1) auxiliary space',
  commonMistakes: [
    'Attempting two pointers inwards on an unsorted array.',
    'Moving both pointers simultaneously when only one should adjust.',
  ],
  defaultInput: {
    array: [1, 2, 4, 7, 11, 15],
    target: 15,
  },
  code: {
    java: `public int[] twoSum(int[] numbers, int target) {
    int left = 0;
    int right = numbers.length - 1;
    while (left < right) {
        int sum = numbers[left] + numbers[right];
        if (sum == target) {
            return new int[]{left, right};
        } else if (sum < target) {
            left++;
        } else {
            right--;
        }
    }
    return new int[]{-1, -1};
}`,
    python: `def two_sum(numbers, target):
    left = 0
    right = len(numbers) - 1
    while left < right:
        curr_sum = numbers[left] + numbers[right]
        if curr_sum == target:
            return [left, right]
        elif curr_sum < target:
            left += 1
        else:
            right -= 1
    return [-1, -1]`,
  },
};

export function generateTwoPointersSteps(arr: number[], target: number): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const n = arr.length;
  const maxVal = Math.max(...arr, 1);

  const getVisualElements = (
    left: number,
    right: number,
    found: boolean = false
  ): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      const labels: string[] = [];

      if (idx === left) {
        state = found ? 'found' : 'comparing';
        labels.push('left');
      }
      if (idx === right) {
        state = found ? 'found' : 'comparing';
        labels.push('right');
      }

      if (idx < left || idx > right) {
        state = 'eliminated';
      }

      return {
        id: `elem-${idx}-${val}`,
        value: val,
        state,
        label: `${idx}`,
        subLabel: labels.join(' & '),
        heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
      };
    });
  };

  let left = 0;
  let right = n - 1;

  steps.push({
    stepIndex: steps.length,
    description: `Initialize Two Pointers: left = 0, right = ${right}, target = ${target}.`,
    elements: getVisualElements(left, right),
    variables: { left, right, sum: null, target },
    codeLine: { java: 2, python: 2 },
    explanation: {
      why: 'Set one pointer at beginning (minimum) and one at end (maximum).',
      whatNext: 'Compute sum = arr[left] + arr[right].',
      keyTakeaway: 'Avoids brute-force O(n²) nested loops by taking advantage of sorted order.',
    },
  });

  while (left < right) {
    const sum = arr[left] + arr[right];

    steps.push({
      stepIndex: steps.length,
      description: `Evaluate sum: arr[${left}] (${arr[left]}) + arr[${right}] (${arr[right]}) = ${sum}. Target is ${target}.`,
      elements: getVisualElements(left, right),
      variables: { left, right, sum, target },
      changedVariables: ['sum'],
      codeLine: { java: 5, python: 5 },
      explanation: {
        why: `Check if current sum equals ${target}.`,
        whatNext:
          sum === target
            ? 'Pair found! Return indices.'
            : sum < target
            ? 'Sum is too small: move left pointer right to increase sum.'
            : 'Sum is too large: move right pointer left to decrease sum.',
        keyTakeaway: 'Because array is sorted, moving left increases sum; moving right decreases sum.',
      },
    });

    if (sum === target) {
      steps.push({
        stepIndex: steps.length,
        description: `MATCH FOUND! Indices [${left}, ${right}] sum to ${target} (${arr[left]} + ${arr[right]}).`,
        elements: getVisualElements(left, right, true),
        variables: { left, right, sum, target, result: `[${left}, ${right}]` },
        changedVariables: ['result'],
        codeLine: { java: 7, python: 7 },
        explanation: {
          why: 'Found pair matching target.',
          whatNext: 'Return pair.',
          keyTakeaway: 'Solved in O(n) time and O(1) space.',
        },
      });
      break;
    } else if (sum < target) {
      left++;
      steps.push({
        stepIndex: steps.length,
        description: `Sum ${sum} < ${target}. Increment left to ${left}.`,
        elements: getVisualElements(left, right),
        variables: { left, right, sum, target },
        changedVariables: ['left'],
        codeLine: { java: 9, python: 9 },
        explanation: {
          why: 'We need a larger sum, so we advance the left pointer.',
          whatNext: 'Recalculate sum.',
          keyTakeaway: 'All pairs with the previous left pointer were too small.',
        },
      });
    } else {
      right--;
      steps.push({
        stepIndex: steps.length,
        description: `Sum ${sum} > ${target}. Decrement right to ${right}.`,
        elements: getVisualElements(left, right),
        variables: { left, right, sum, target },
        changedVariables: ['right'],
        codeLine: { java: 11, python: 11 },
        explanation: {
          why: 'We need a smaller sum, so we retreat the right pointer.',
          whatNext: 'Recalculate sum.',
          keyTakeaway: 'All pairs with the previous right pointer were too large.',
        },
      });
    }
  }

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
