import { AlgorithmMetadata, AlgorithmStep, VisualElement } from '../../../types/algorithm';

export const mergeSortMetadata: AlgorithmMetadata = {
  id: 'merge-sort',
  title: 'Merge Sort',
  category: 'BEGINNER',
  subcategory: 'Sorting Algorithms',
  difficulty: 'Medium',
  description:
    'A classic divide-and-conquer algorithm that continuously splits the array into halves until single-element subarrays are reached, then merges them back in sorted order.',
  realWorldExample:
    'Merging two sorted decks of cards: you compare the top card of each deck and place the smaller one down face-up, repeating until both decks are exhausted.',
  timeComplexity: {
    best: 'O(n log n)',
    average: 'O(n log n)',
    worst: 'O(n log n) (guaranteed)',
  },
  spaceComplexity: 'O(n) auxiliary space for merging',
  commonMistakes: [
    'Forgetting that Merge Sort requires O(n) auxiliary memory unlike in-place quicksort.',
    'Incorrect calculation of midpoint (overflow in low + high).',
    'Off-by-one errors in copy back loops from temp array.',
  ],
  defaultInput: [38, 27, 43, 3, 9, 82, 10],
  code: {
    java: `public void mergeSort(int[] arr, int l, int r) {
    if (l < r) {
        int m = l + (r - l) / 2;
        mergeSort(arr, l, m);
        mergeSort(arr, m + 1, r);
        merge(arr, l, m, r);
    }
}`,
    python: `def merge_sort(arr, l, r):
    if l < r:
        m = (l + r) // 2
        merge_sort(arr, l, m)
        merge_sort(arr, m + 1, r)
        merge(arr, l, m, r)`,
  },
};

export function generateMergeSortSteps(initialArr: number[]): AlgorithmStep[] {
  const steps: AlgorithmStep[] = [];
  const arr = [...initialArr];
  const n = arr.length;
  const maxVal = Math.max(...arr, 1);

  const buildElements = (
    leftIdx: number | null,
    rightIdx: number | null,
    activeRange?: [number, number]
  ): VisualElement[] => {
    return arr.map((val, idx) => {
      let state: VisualElement['state'] = 'default';
      const labels: string[] = [];

      if (activeRange && idx >= activeRange[0] && idx <= activeRange[1]) {
        state = 'active';
      }

      if (idx === leftIdx) {
        state = 'comparing';
        labels.push('p1');
      }
      if (idx === rightIdx) {
        state = 'swapping';
        labels.push('p2');
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

  steps.push({
    stepIndex: steps.length,
    description: `Start Merge Sort on array of ${n} elements.`,
    elements: buildElements(null, null),
    variables: { l: 0, r: n - 1, m: null },
    codeLine: { java: 1, python: 1 },
    explanation: {
      why: 'Divide and conquer strategy begins.',
      whatNext: 'Recursively subdivide array until subarrays have size 1.',
      keyTakeaway: 'Merge Sort guarantees O(n log n) even in worst-case scenarios.',
    },
  });

  function merge(l: number, m: number, r: number) {
    steps.push({
      stepIndex: steps.length,
      description: `Merging sorted subarrays [${l} ... ${m}] and [${m + 1} ... ${r}].`,
      elements: buildElements(null, null, [l, r]),
      variables: { l, m, r },
      changedVariables: ['l', 'm', 'r'],
      codeLine: { java: 6, python: 6 },
      explanation: {
        why: 'Both left and right halves are individually sorted.',
        whatNext: 'Compare front elements of each half and place smaller element first.',
        keyTakeaway: 'Two-finger algorithm merges in linear O(k) time where k is segment length.',
      },
    });

    const left = arr.slice(l, m + 1);
    const right = arr.slice(m + 1, r + 1);
    let i = 0;
    let j = 0;
    let k = l;

    while (i < left.length && j < right.length) {
      const leftVal = left[i];
      const rightVal = right[j];

      steps.push({
        stepIndex: steps.length,
        description: `Compare left element ${leftVal} with right element ${rightVal}.`,
        elements: buildElements(l + i, m + 1 + j, [l, r]),
        variables: { l, r, leftVal, rightVal, k },
        codeLine: { java: 6, python: 6 },
        explanation: {
          why: `Compare current elements from both sorted halves.`,
          whatNext: leftVal <= rightVal ? `Place ${leftVal} into position ${k}.` : `Place ${rightVal} into position ${k}.`,
          keyTakeaway: 'Stable merging: if equal, left half element takes precedence.',
        },
      });

      if (leftVal <= rightVal) {
        arr[k] = leftVal;
        i++;
      } else {
        arr[k] = rightVal;
        j++;
      }
      k++;

      steps.push({
        stepIndex: steps.length,
        description: `Placed ${arr[k - 1]} at merged index ${k - 1}.`,
        elements: buildElements(null, null, [l, r]),
        variables: { l, r, k: k - 1, placedVal: arr[k - 1] },
        changedVariables: ['placedVal'],
        codeLine: { java: 6, python: 6 },
        explanation: {
          why: `Element placed into correct relative position.`,
          whatNext: 'Advance pointers.',
          keyTakeaway: 'Temporary array / buffer ensures stability.',
        },
      });
    }

    while (i < left.length) {
      arr[k] = left[i];
      i++;
      k++;
    }

    while (j < right.length) {
      arr[k] = right[j];
      j++;
      k++;
    }

    steps.push({
      stepIndex: steps.length,
      description: `Merged range [${l} ... ${r}] complete: [${arr.slice(l, r + 1).join(', ')}].`,
      elements: buildElements(null, null, [l, r]),
      variables: { l, r, rangeSorted: true },
      codeLine: { java: 6, python: 6 },
      explanation: {
        why: 'All elements from both halves merged.',
        whatNext: 'Return from recursive call.',
        keyTakeaway: `Range [${l}...${r}] is now fully sorted.`,
      },
    });
  }

  function sort(l: number, r: number) {
    if (l < r) {
      const m = Math.floor(l + (r - l) / 2);

      steps.push({
        stepIndex: steps.length,
        description: `Divide subarray [${l} ... ${r}] at midpoint m = ${m}.`,
        elements: buildElements(null, null, [l, r]),
        variables: { l, r, m },
        changedVariables: ['l', 'r', 'm'],
        codeLine: { java: 3, python: 3 },
        explanation: {
          why: `Subdivide problem into two subproblems of size ~${Math.ceil((r - l + 1) / 2)}.`,
          whatNext: `Sort left half [${l} ... ${m}].`,
          keyTakeaway: 'Recursion tree has depth log2(n).',
        },
      });

      sort(l, m);
      sort(m + 1, r);
      merge(l, m, r);
    }
  }

  sort(0, n - 1);

  steps.push({
    stepIndex: steps.length,
    description: `Merge Sort complete! Array is sorted: [${arr.join(', ')}].`,
    elements: arr.map((val, idx) => ({
      id: `elem-${idx}-${val}`,
      value: val,
      state: 'sorted',
      label: `${idx}`,
      subLabel: 'sorted',
      heightPercent: Math.max(20, Math.min(100, (val / maxVal) * 100)),
    })),
    variables: { l: 0, r: n - 1, complete: true },
    codeLine: { java: 7, python: 6 },
    explanation: {
      why: 'All sub-arrays merged together.',
      whatNext: 'Done.',
      keyTakeaway: 'Merge sort runs in O(n log n) time and is widely used in external sorting.',
    },
  });

  steps.forEach((s) => (s.totalSteps = steps.length));
  return steps;
}
